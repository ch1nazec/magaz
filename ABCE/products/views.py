from rest_framework import (viewsets,
                            permissions,
                            generics, views)
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product, Category
from .serializer import (ProductSerializer,
                         CategoryListSerializer,
                        CategorySerializer)


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        return CategorySerializer
    
    def get_permissions(self):
        if self.action in {'create', 'destroy', 'update', 'partial_update'}:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
    @action(detail=False, methods=['get'])
    def tree(self, request):
        categories = Category.objects.filter(parent__isnull=True)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)