from rest_framework import (viewsets,
                            permissions,)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import Product, Category, ImageProduct, Color, Size, ProductVariant, Tag, TagToProduct
from .serializer import (ProductSerializer, ImageProductSerializer,
                         CategoryListSerializer, ColorSerializer,
                        CategorySerializer, SizeSerializer,
                        TagToProductSerializer, TagSerializer, ProductVariantSerializer)
from others.permissions import BaseAdminViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import ProductVariantFilter


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['name', 'description']
    filterset_fields = ['gender', 'category_id', 'name', 'is_active', 'brand']
    ordering_fields = ['name', 'gender', 'product_model__name', 'product_model__brand__name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]

class ProductVariantViewSet(BaseAdminViewSet):
    serializer_class = ProductVariantSerializer
    queryset = ProductVariant.objects.all().select_related(
        'product',
        'product__category',
        'product__brand',
        'product__model',
        'color',
        'size')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductVariantFilter
    search_fields = ['product__name']
    ordering_fields = ['product__name', 'price']
    ordering = ['product__name']


class CategoryViewSet(BaseAdminViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        return CategorySerializer
    
    @action(detail=False, methods=['get'])
    def tree(self, request):
        categories = Category.objects.filter(parent__isnull=True)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class ImagesViewSet(BaseAdminViewSet):
    queryset = ImageProduct.objects.all()
    serializer_class = ImageProductSerializer

    def get_queryset(self):
        queryset = ImageProduct.objects.all().select_related('product', 'color')
        
        product_id = self.request.query_params.get('product')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        
        color_id = self.request.query_params.get('color')
        if color_id:
            queryset = queryset.filter(color_id=color_id)

        return queryset
    
    @action(detail=False, methods=['post'], url_path='upload-multiple')
    def upload_multiple(self, request):
        images = request.FILES.getlist('images')
        product_id = request.data.get('product_id')

        if not product_id:
            return Response(data={
                'error': 'product_id обязателен!'
            }, status=status.HTTP_400_BAD_REQUEST)

        all_images = []
        for image in images:
            img = ImageProduct.objects.create(
                product_id=product_id,
                image=image,
                image_type=request.data.get('image_type', 'gallery'))
            all_images.append(img)
        
        serializer = self.get_serializer(all_images, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def set_main(self, request, pk=None):
        image = self.get_object()

        ImageProduct.objects.filter(
            product=image.product,
            is_main=True,
        ).exclude(pk=image.pk).update(is_main=False)

        image.is_main = True
        image.save()
        return Response({'status': 'Success!'})
    

class ColorViewSet(BaseAdminViewSet):
    serializer_class = ColorSerializer
    queryset = Color.objects.all()


class SizeViewSet(BaseAdminViewSet):
    serializer_class = SizeSerializer
    queryset = Size.objects.all()


class TagViewSet(BaseAdminViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class TagToProductViewSet(BaseAdminViewSet):
    serializer_class = TagToProductSerializer
    queryset = TagToProduct.objects.all()