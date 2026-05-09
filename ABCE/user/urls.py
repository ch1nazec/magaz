from django.urls import path
from .views import (
    UserListAPI, logout_view,
    RegisterView, TelegramLinkUserView,
    LoginView, UserDetailView,
    ChangePasswordView, ProfileView, UpdateUserView)


urlpatterns = [
    path('', UserListAPI.as_view(), name='user-list'),
    path('detail/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('change-password/', ChangePasswordView.as_view(), name='user-change-password'),
    path('logout/', logout_view, name='user-logout'),
    path('telegram-link/<int:tg_id>', TelegramLinkUserView.as_view(), name='user-telegram'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', UpdateUserView.as_view(), name='profile-update'),
]
