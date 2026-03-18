from rest_framework import serializers
from rest_framework import status
from .models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'phone_number', 'status',
            'comment', 'address', 'created_at', 'updated_at',
            'total_amount'
        ]
        read_only_fields = ['id', 'user', 'phone_number', 'comment',
                            'address', 'created_at', 'updated_at',
                            'total_amount']


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = [
            'order', 'product', 'color',
            'size', 'price', 'quantity'
        ]