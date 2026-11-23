from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    BrandViewSet,
    VehicleMakeViewSet,
    VehicleModelViewSet,
    VehicleGenerationViewSet,
    VehicleModificationViewSet,
    ProductViewSet,
    ProductArticleViewSet,
    ProductImageViewSet,
    WarehouseViewSet,
    StockViewSet,
)

router = DefaultRouter()

router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"brands", BrandViewSet, basename="brand")

router.register(r"makes", VehicleMakeViewSet, basename="make")
router.register(r"models", VehicleModelViewSet, basename="model")
router.register(r"generations", VehicleGenerationViewSet, basename="generation")
router.register(r"modifications", VehicleModificationViewSet, basename="modification")

router.register(r"products", ProductViewSet, basename="product")
router.register(r"articles", ProductArticleViewSet, basename="article")
router.register(r"images", ProductImageViewSet, basename="image")

router.register(r"warehouses", WarehouseViewSet, basename="warehouse")
router.register(r"stocks", StockViewSet, basename="stock")

urlpatterns = [
    path("", include(router.urls)),
]