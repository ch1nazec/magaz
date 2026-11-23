from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser, OTPCode


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    ordering = ("-created_at",)
    list_display = ("id", "email", "username", "phone_number",
                    "first_name", "last_name", "is_active",
                    "is_staff", "created_at")
    list_filter = ("is_active", "is_staff", "is_superuser", "created_at")
    search_fields = ("email", "username", "phone_number",
                     "first_name", "last_name", "telegram_id")
    readonly_fields = ("created_at", "updated_at", "last_login", "date_joined")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Личные данные", {"fields": ("username", "first_name", "last_name",
                                      "phone_number", "address", "telegram_id")}),
        ("Права", {"fields": ("is_active", "is_staff", "is_superuser",
                              "groups", "user_permissions")}),
        ("OTP", {"fields": ("otp_hash", "otp_created_at", "otp_attempts"),
                 "classes": ("collapse",)}),
        ("Даты", {"fields": ("last_login", "date_joined",
                             "created_at", "updated_at")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "phone_number",
                       "first_name", "password1", "password2",
                       "is_active", "is_staff"),
        }),
    )


@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "phone", "code", "created_at", "is_used")
    list_filter = ("is_used", "created_at")
    search_fields = ("phone", "code")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"