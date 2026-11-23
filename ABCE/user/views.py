from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializer import (
    ForgotPasswordSerializer,
    LoginUserSerializer,
    PasswordChangeSerializer,
    RegistartionUserSerializer,
    ResetPasswordSerializer,
    UpdateUserSerializer,
    UserSerializer,
)
from .tasks import send_email_task


# ====================== Throttling ======================

class LoginThrottling(AnonRateThrottle):
    scope = "login"

class RegisterThrottling(AnonRateThrottle):
    scope = "register"


class ForgotPasswordThrottling(AnonRateThrottle):
    scope = "forgot_password"


class ForgotPasswordEmailThrottling(AnonRateThrottle):
    scope = "forgot_password_email"

    def get_cache_key(self, request, view):
        email = (request.data.get("email") or "").lower().strip()
        if not email:
            return None
        return self.cache_format % {"scope": self.scope, "ident": email}


class ResetPasswordThrottling(AnonRateThrottle):
    scope = "reset_password"


# ====================== Админка пользователей ======================

class UserListAPI(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"


# ====================== Авторизация и профиль ======================

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegistartionUserSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [RegisterThrottling]

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        refresh = RefreshToken.for_user(user=user)

        return Response(
            {
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "Пользователь успешно зарегистрирован",
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [LoginThrottling]

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response({
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "message": "Вы успешно зашли!",
        })


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UpdateUserView(generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response({"message": "Данные были успешно изменены"})


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(
            {"message": "Пароль успешно сменили."},
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request: Request):
    """Выход юзера"""
    refresh_token = request.data.get("refresh_token")
    if not refresh_token:
        return Response(
            {"error": "Требуется refresh_token"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Успешно вышли!"}, status=status.HTTP_200_OK)
    except Exception:
        return Response(
            {"error": "Неверный или уже отозванный токен"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# ====================== Сброс пароля по почте ======================

class ForgotPassword(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ForgotPasswordThrottling, ForgotPasswordEmailThrottling]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        user = CustomUser.objects.filter(email=email).first()

        if user:
            try:
                send_email_task.delay(user_id=user.pk)
            except Exception:
                user.clear_otp()
                user.save(update_fields=["otp_hash", "otp_created_at", "otp_attempts"])

        return Response(
            {"detail": "Если указанный email зарегистрирован, код отправлен на почту."},
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@throttle_classes([ResetPasswordThrottling])
@transaction.atomic
def reset_password(request: Request):
    serializer = ResetPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    user = CustomUser.objects.select_for_update().filter(email=data["email"]).first()
    otp_code = data.get("otp_code")

    if not user or not user.verify_otp(otp_code):
        if user:
            user.save(update_fields=["otp_attempts", "otp_hash", "otp_created_at"])
        return Response(
            {"error": "Неверный или просроченный код."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.set_password(data["new_password"])
    user.clear_otp()
    user.save(update_fields=["password", "otp_hash", "otp_created_at", "otp_attempts"])

    return Response({"detail": "Пароль обновлён."}, status=status.HTTP_200_OK)
