from rest_framework import permissions
from django.conf import settings


class IsAdminOrBot(permissions.BasePermission):
    def has_permission(self, request, view):
        token = request.headers.get('X-Bot-Token')
        
        if request.user and request.user.is_authenticated and request.user.is_staff:
            return True
        
        return token == settings.BOT_API