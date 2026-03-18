from rest_framework import serializers
from .models import Order, OrderItem
from re import fullmatch


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['product', 'color',
            'size', 'price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'phone_number', 'status',
            'comment', 'address', 'created_at', 'updated_at',
            'total_amount', 'items',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at',]
    
    def validate_phone_number(self, value):
        if fullmatch(r'^(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$', value):
            return value
        else:
            raise serializers.ValidationError(f'Номер {value} неверный. Только российские номера')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)