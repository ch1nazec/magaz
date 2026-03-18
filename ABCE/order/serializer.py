from rest_framework import serializers
from rest_framework import status
from .models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'user', 'phone_number', 'status',
            'comment', 'address', 'created_at', 'updated_at',
            'total_amount'
        ]
        read_only_fields = ['user', 'phone_number', 'comment',
                            'address', 'created_at', 'updated_at',
                            'total_amount']