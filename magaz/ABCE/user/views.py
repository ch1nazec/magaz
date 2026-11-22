import hashlib
import hmac
from django_filters.rest_framework import DjangoFilterBackend

from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializer import (UserSerializer, RegistartionUserSerializer,
                         LoginUserSerializer, PasswordChangeSerializer, UpdateUserSerializer, ResetPasswordSerializer, ForgotPasswordSerializer)

from others.decorators import auto_clear_cache, set_cache, auto_set_cache

from django.db import transaction
from rest_framework.throttling import AnonRateThrottle
from django.core.mail import send_mail

from .tasks import send_email_task


def verify_telegram(data):
    tg_hash = data.get('hash')

    if not tg_hash:
        return False

    # Исключаем hash из проверяемых данных
    data_check_list = [
        f'{key}={value}'
        for key, value in data.items()
        if key != 'hash'
    ]

    # Сортируем по ключам и объединяем через перевод строки
    data_check_string = '\n'.join(
        sorted(data_check_list, key=lambda item: item.split('=', 1)[0])
    )

    # Секретный ключ для проверки Telegram Mini App initData
    secret_key = hmac.new(
        b'WebAppData',
        settings.BOT_API.encode('utf-8'),
        hashlib.sha256
    ).digest()

    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(calculated_hash, tg_hash)


class ForgotPasswordThrottling(AnonRateThrottle):
    scope = 'forgot_password'

class ForgotPasswordEmailThrottling(AnonRateThrottle):
    scope = 'forgot_password_email'

    def get_cache_key(self, request, view):
        email = (request.data.get('email') or '').lower().strip()
        if not email:
            return
        return self.cache_format % {"scope": self.scope, "ident": email}


class ResetPasswordThrottling(AnonRateThrottle):
    scope = 'reset_password'


# Create your views here.
class UserListAPI(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]


@auto_clear_cache(pattern='user_*')
@auto_set_cache(pattern='user_')
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegistartionUserSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        Refresh = RefreshToken.for_user(user=user)

        return Response(
            {
                'user': UserSerializer(user).data,
                'refresh': str(Refresh),
                'access': str(Refresh.access_token),
                'message': 'Пользователь успешно зарегистрирован'
            }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Вы успешно зашли!'
        })


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request: Request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response({
            'message': 'Пароль успешно сменили.'
        }, status=status.HTTP_200_OK)


class UpdateUserView(generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request: Request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response({'message': 'Данные были успешно изменены'})


class TelegramLinkUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request):
        data = request.data
        user = request.user

        if not verify_telegram(data):
            return Response({"error": "Неверная подпись данных"}, status=status.HTTP_400_BAD_REQUEST)
        tg_verify_id = data.get('id')

        if user.telegram_id == tg_verify_id:
            return Response({'error': 'Не нужно, вы уже привязали аккаунт.'}, status=status.HTTP_400_BAD_REQUEST)

        check = CustomUser.objects.filter(telegram_id=tg_verify_id).first()
        if check:
            return Response({'error': 'Пользователь уже привязан к другому аккаунту.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.telegram_id = tg_verify_id
        user.save()

        return Response({'message': 'Связка произошла успешно'}, status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
@permission_classes(permission_classes=[permissions.IsAuthenticated])
def logout_view(request: Request):
    """Выход юзера"""

    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Успешно вышли!'})
    except:
        return Response({'error': 'Invalid token'})
    

class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user




class ForgotPassword(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ForgotPasswordThrottling, ForgotPasswordEmailThrottling]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = CustomUser.objects.get(email=serializer.validated_data.get('email'))
        except CustomUser.DoesNotExist as error:
            return Response({'detail': 'Code has been sent on your email.'}, status=status.HTTP_200_OK)
        
        try:
            send_email_task.delay(user_id=user.pk)

        except Exception as error:
            user.clear_otp()
            user.save(update_fields=["otp_hash", "otp_created_at", "otp_attempts"])

        return Response(
            {"detail": "Code was been sent on your email."},
            status=status.HTTP_200_OK,
        )


@api_view(['POST'])
@transaction.atomic
def reset_password(request: Request):
    serializer = ResetPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    user = CustomUser.objects.select_for_update().filter(email=data["email"]).first()

    otp_code = data.get('otp_code')
    if not user.verify_otp(otp_code):
        return Response({
            'error': 'Неверный/просроченный код.'
        }, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(data.get('new_password'))

    user.clear_otp()
    user.save(update_fields=["password",
            "otp_hash",
            "otp_created_at",
            "otp_attempts"])

    return Response({"detail": "Пароль обновлён."}, status=status.HTTP_200_OK)