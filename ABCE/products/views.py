from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Min, OuterRef, Prefetch, Subquery, Sum
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import (
    Category, Brand, Product, ProductArticle, ProductImage,
    VehicleMake, VehicleModel, VehicleGeneration, VehicleModification,
    PartApplicability, Warehouse, Stock
)
from .serializer import (
    CategorySerializer, CategoryListSerializer, BrandSerializer,
    VehicleMakeSerializer, VehicleModelSerializer,
    VehicleGenerationSerializer, VehicleModificationSerializer,
    ProductListSerializer, ProductDetailSerializer, ProductWriteSerializer,
    ProductArticleSerializer, ProductImageSerializer,
    WarehouseSerializer, StockSerializer
)
from .filters import ProductFilter, StockFilter

class BaseAdminViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

# Категории

class CategoryViewSet(BaseAdminViewSet):
    queryset = Category.objects.all()
    lookup_field = "slug"
    pagination_class = None

    def get_serializer_class(self):
        if self.action == "list":
            return CategoryListSerializer
        return CategorySerializer

    @action(detail=False, methods=["get"])
    def tree(self, request):
        roots = Category.objects.filter(parent=None).prefetch_related("children")
        serializer = CategorySerializer(roots, many=True, context={"request": request})
        return Response(serializer.data)

# Бренды 

class BrandViewSet(BaseAdminViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering = ["name"]

# Автомобили

class VehicleMakeViewSet(BaseAdminViewSet):
    queryset = VehicleMake.objects.all()
    serializer_class = VehicleMakeSerializer
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering = ["name"]

class VehicleModelViewSet(BaseAdminViewSet):
    queryset = VehicleModel.objects.select_related("make")
    serializer_class = VehicleModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["make", "make__slug"]
    search_fields = ["name"]
    ordering = ["make__name", "name"]

class VehicleGenerationViewSet(BaseAdminViewSet):
    queryset = VehicleGeneration.objects.select_related("model__make")
    serializer_class = VehicleGenerationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["model", "model__slug", "model__make__slug"]
    ordering = ["-year_from"]

class VehicleModificationViewSet(BaseAdminViewSet):
    queryset = VehicleModification.objects.select_related("generation__model__make")
    serializer_class = VehicleModificationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["generation", "fuel", "drive"]
    search_fields = ["name", "engine_code"]
    ordering = ["name"]

# Товары

class ProductViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "article", "articles__number", "brand__name"]
    ordering_fields = ["name", "article", "created_at", "price", "quantity"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return ProductWriteSerializer
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductListSerializer

    def get_queryset(self):
        qs = (
            Product.objects
            .filter(is_active=True)
            .select_related("brand", "category")
        )

        if self.action == "retrieve":
            qs = qs.prefetch_related(
                Prefetch(
                    "images",
                    queryset=ProductImage.objects.order_by("order", "-is_main"),
                ),
                "articles",
                "stocks__warehouse",
                "applicabilities__modification__generation__model__make",
            )
        else:
            qs = qs.prefetch_related(
                Prefetch(
                    "images",
                    queryset=ProductImage.objects.order_by("order", "-is_main"),
                    to_attr="prefetched_images"
                )
            )

        warehouse_id = self.request.query_params.get("warehouse")
        city = self.request.query_params.get("city")

        has_valid_warehouse = bool(warehouse_id and warehouse_id.isdigit())

        if has_valid_warehouse or city:
            stock_qs = Stock.objects.all()
            if has_valid_warehouse:
                stock_qs = stock_qs.filter(warehouse_id=int(warehouse_id))
            if city:
                stock_qs = stock_qs.filter(warehouse__city__iexact=city)

            stock_subquery = stock_qs.filter(product=OuterRef("pk")).order_by("id")

            qs = qs.annotate(
                price=Subquery(stock_subquery.values("price")[:1]),
                price_old=Subquery(stock_subquery.values("price_old")[:1]),
                quantity=Subquery(stock_subquery.values("quantity")[:1]),
            )
        else:
            qs = qs.annotate(
                price=Min("stocks__price"),
                quantity=Sum("stocks__quantity"),
            )

        return qs.distinct()


# Остальное

class ProductArticleViewSet(BaseAdminViewSet):
    queryset = ProductArticle.objects.select_related("product")
    serializer_class = ProductArticleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["product", "type", "is_main"]
    search_fields = ["number"]

class ProductImageViewSet(BaseAdminViewSet):
    queryset = ProductImage.objects.select_related("product")
    serializer_class = ProductImageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["product", "image_type", "is_main"]

class WarehouseViewSet(BaseAdminViewSet):
    queryset = Warehouse.objects.filter(is_active=True)
    serializer_class = WarehouseSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "city"]
    ordering = ["sort_order", "city"]

class StockViewSet(BaseAdminViewSet):
    queryset = Stock.objects.select_related("product", "warehouse")
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = StockFilter
    ordering_fields = ["price", "quantity", "updated_at"]
    ordering = ["-updated_at"]