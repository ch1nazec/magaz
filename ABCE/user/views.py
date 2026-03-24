from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializer import (UserSerializer, RegistartionUserSerializer,
                         LoginUserSerializer, PasswordChangeSerializer)


# Create your views here.
class UserListAPI(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegistartionUserSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
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

    def post(self, request, *args, **kwargs):
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

    def update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response({
            'message': 'Пароль успешно сменили.'
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes(permission_classes=[permissions.IsAuthenticated])
def logout_view(request):
    """Выход юзера"""

    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Успешно вышли!'})
    except:
        return Response(
            {'error': 'Invalid token'}
        )