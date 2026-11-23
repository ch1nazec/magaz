from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "article",
            "product_name",
            "warehouse_name",
            "price",
            "quantity",
            "total_price",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "status_display",
            "phone_number",
            "address",
            "comment",
            "warehouse",
            "total_amount",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["status", "total_amount", "warehouse", "created_at", "updated_at"]


class CreateOrderSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=16)
    address = serializers.CharField(max_length=500)
    comment = serializers.CharField(max_length=1000, required=False, allow_blank=True)