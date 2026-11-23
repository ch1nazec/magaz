from django.urls import path
from .views import (
    ChangePasswordView,
    ForgotPassword,
    LoginView,
    ProfileView,
    RegisterView,
    UpdateUserView,
    UserDetailView,
    UserListAPI,
    logout_view,
    reset_password,
)

urlpatterns = [
    path("", UserListAPI.as_view(), name="user-list"),
    path("detail/<int:id>/", UserDetailView.as_view(), name="user-detail"),
    path("register/", RegisterView.as_view(), name="user-register"),
    path("login/", LoginView.as_view(), name="user-login"),
    path("change-password/", ChangePasswordView.as_view(), name="user-change-password"),
    path("logout/", logout_view, name="user-logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/update/", UpdateUserView.as_view(), name="profile-update"),
    path("forget-password/", ForgotPassword.as_view(), name="forget-password"),
    path("reset-password/", reset_password, name="reset-password"),
]
