from django.urls import path
from .views import (
    UserListAPI, logout_view,
    RegisterView,
    LoginView,
    ChangePasswordView
)


urlpatterns = [
    path('', UserListAPI.as_view(), name='user-list'),
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('change-password/', ChangePasswordView.as_view(), name='user-change-password'),
]
