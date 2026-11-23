import secrets

from rest_framework import permissions
from django.conf import settings


class IsAdminOrBot(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.is_staff:
            return True

        incoming_token = request.headers.get("X-Bot-Token")
        expected_token = getattr(settings, "BOT_API", None)

        if not incoming_token or not expected_token:
            return False

        return secrets.compare_digest(str(incoming_token), str(expected_token))