from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ProductViewSet,
                    CategoryViewSet, ImagesViewSet, ColorViewSet,
                    SizeViewSet, ProductVariantViewSet, TagViewSet,
                    TagToProductViewSet, BrandViewSet, ProductForCategory,
                    ProductModelFindViewSet,
                    )


router = DefaultRouter()

router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'images', ImagesViewSet)
router.register(r'colors', ColorViewSet)
router.register(r'sizes', SizeViewSet)
router.register(r'productvariants', ProductVariantViewSet)
router.register(r'tags', TagViewSet)
router.register(r'tagtoproducts', TagToProductViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'products-group', ProductModelFindViewSet, basename='products-group')


urlpatterns = [
    path('', include(router.urls), name='product'),
    path('product-category/<slug:category_slug>/', ProductForCategory.as_view(), name='product-category')
]