from rest_framework import (viewsets,
                            permissions,)


class BaseAdminViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in {'create', 'destroy', 'update', 'partial_update'}:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]