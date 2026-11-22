from rest_framework import serializers
from .models import Order, OrderItem
from re import fullmatch


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'color',
            'size', 'price', 'quantity']
    def validate_price(self, attr):
        if attr < 0:
            return serializers.ValidationError('Цена не может быть меньше 0')
        return attr
    def validate_quantity(self, attr):
        if attr < 0:
            return serializers.ValidationError('Количество продукта не может равнятся 0')
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    status = serializers.CharField(source='get_status_display', read_only=True)
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'first_name', 'last_name', 'phone_number', 'status',
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