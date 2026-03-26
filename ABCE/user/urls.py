from django.urls import path
from .views import (
    UserListAPI, logout_view,
    RegisterView, TelegramLinkUserView,
    LoginView,
    ChangePasswordView
)


urlpatterns = [
    path('', UserListAPI.as_view(), name='user-list'),
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('change-password/', ChangePasswordView.as_view(), name='user-change-password'),
    path('logout/', logout_view, name='user-logout'),
    path('telegram-link/<int:tg_id>', TelegramLinkUserView.as_view(), name='user-telegram'),
]
