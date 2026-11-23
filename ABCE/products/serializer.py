from rest_framework import serializers
from .models import (
    Category, Brand, Product, ProductArticle, ProductImage,
    VehicleMake, VehicleModel, VehicleGeneration, VehicleModification,
    PartApplicability, Warehouse, Stock
)

# Категории

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "image", "image_url", "parent", "children"]

    def get_children(self, obj):
        qs = obj.get_children()
        return CategorySerializer(qs, many=True, context=self.context).data if qs.exists() else []

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url") and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "image"]

#Бренды
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "slug", "logo"]

#  Автомобили 
class VehicleMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleMake
        fields = ["id", "name", "slug", "logo"]

class VehicleModelSerializer(serializers.ModelSerializer):
    make_name = serializers.CharField(source="make.name", read_only=True)

    class Meta:
        model = VehicleModel
        fields = ["id", "name", "slug", "make", "make_name"]

class VehicleGenerationSerializer(serializers.ModelSerializer):
    model_name = serializers.CharField(source="model.name", read_only=True)
    make_name = serializers.CharField(source="model.make.name", read_only=True)

    class Meta:
        model = VehicleGeneration
        fields = ["id", "name", "year_from", "year_to", "body", "model", "model_name", "make_name"]

class VehicleModificationSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = VehicleModification
        fields = [
            "id", "name", "engine_code", "engine_volume", "fuel",
            "transmission", "drive", "year_from", "year_to",
            "generation", "full_name"
        ]

    def get_full_name(self, obj):
        return str(obj)

# Товар
class ProductArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductArticle
        fields = ["id", "number", "type", "brand_name", "is_main"]

class ProductImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ["id", "url", "image_type", "is_main", "order"]

    def get_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class StockShortSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source="warehouse.city", read_only=True)
    warehouse_name = serializers.CharField(source="warehouse.name", read_only=True)

    class Meta:
        model = Stock
        fields = ["id", "warehouse", "warehouse_name", "city", "quantity", "price", "price_old"]

class ProductListSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category_slug = serializers.CharField(source="category.slug", read_only=True)
    main_image = serializers.SerializerMethodField()

    # Эти поля появляются только когда выбран склад/город
    price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, required=False)
    quantity = serializers.IntegerField(read_only=True, required=False)
    price_old = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, required=False)

    class Meta:
        model = Product
        fields = [
            "id", "article", "name", "slug",
            "brand", "category_slug",
            "is_new", "is_bestseller",
            "main_image",
            "price", "price_old", "quantity",
        ]

    def get_main_image(self, obj):
        images = getattr(obj, "prefetched_images", None)
        if images is None:
            images = list(obj.images.all())

        main = next((img for img in images if img.is_main), None)
        if not main and images:
            main = images[0]

        if main and main.image:
            request = self.context.get("request")
            return request.build_absolute_uri(main.image.url) if request else main.image.url
        return None

class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategoryListSerializer(read_only=True)
    articles = ProductArticleSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    stocks = StockShortSerializer(many=True, read_only=True)
    applicabilities = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "article", "name", "slug", "description", "attributes",
            "brand", "category",
            "is_active", "is_new", "is_bestseller",
            "articles", "images", "stocks", "applicabilities",
            "created_at", "updated_at",
        ]

    def get_applicabilities(self, obj):
        apps = obj.applicabilities.select_related(
            "modification__generation__model__make"
        ).all()
        return [
            {
                "id": a.id,
                "note": a.note,
                "is_confirmed": a.is_confirmed,
                "modification": str(a.modification),
                "modification_id": a.modification_id,
            }
            for a in apps
        ]

class ProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "article", "name", "description", "attributes",
            "category", "brand",
            "is_active", "is_new", "is_bestseller",
        ]

# Остальное
class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ["id", "name", "city", "address", "is_active", "sort_order"]

class StockSerializer(serializers.ModelSerializer):
    product_article = serializers.CharField(source="product.article", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)
    city = serializers.CharField(source="warehouse.city", read_only=True)

    class Meta:
        model = Stock
        fields = [
            "id", "product", "product_article", "product_name",
            "warehouse", "city",
            "quantity", "price", "price_old", "updated_at"
        ]