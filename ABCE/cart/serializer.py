from rest_framework import serializers
from django.db import transaction
from products.models import Product, Warehouse, Stock
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_active=True),
        source="product",
        write_only=True
    )
    warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.filter(is_active=True),
        source="warehouse",
        write_only=True
    )

    # Для чтения
    article = serializers.CharField(source="product.article", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_slug = serializers.CharField(source="product.slug", read_only=True)
    warehouse_name = serializers.CharField(source="warehouse.name", read_only=True)
    city = serializers.CharField(source="warehouse.city", read_only=True)
    main_image = serializers.SerializerMethodField()
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product_id", "warehouse_id",
            "article", "product_name", "product_slug",
            "warehouse_name", "city",
            "quantity", "price", "total_price",
            "main_image",
        ]
        read_only_fields = ["price"]

    def get_main_image(self, obj):
        image = obj.product.images.filter(is_main=True).first()
        if not image:
            image = obj.product.images.first()
        if image and image.image:
            request = self.context.get("request")
            return request.build_absolute_uri(image.image.url) if request else image.image.url
        return None

    def validate(self, data):
        product = data.get("product") or self.instance.product
        warehouse = data.get("warehouse") or self.instance.warehouse
        quantity = data.get("quantity", 1)

        try:
            stock = Stock.objects.get(product=product, warehouse=warehouse)
        except Stock.DoesNotExist:
            raise serializers.ValidationError("Товар отсутствует на выбранном складе")

        if quantity > stock.quantity:
            raise serializers.ValidationError(
                f"Недостаточно товара. В наличии: {stock.quantity} шт."
            )

        # Подставляем актуальную цену
        data["price"] = stock.price
        return data

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price", "total_items", "updated_at"]