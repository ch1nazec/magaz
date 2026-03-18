from rest_framework import serializers
from .models import (Category, Brand, ProductModel,
                     Product, Color, Size,
                     ProductVariant, ImageProduct, Tag,
                     TagToProduct)
from django.db import models
from decimal import Decimal


def check_name(name, value):
    """Проверка название без цифр"""
    if value.isalpha():
            return value
    else:
        raise serializers.ValidationError(f'{name} не может называться цифрами.')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'name', 'image',
            'parent',
        ]
    
    def validate_name(self, value: str) -> str:
        return check_name(name='Категория', value=value)
    
    def get_children(self, obj):
        serializer = CategorySerializer(instance=obj.children.all(), many=True)
        return serializer.data


class BrandSerializer(serializers.ModelSerializer):
    """Сериализатор брендов"""
    class Meta:
        model = Brand
        fields = [
            'name',
            'logo'
        ]


class ProductModelSerializer(serializers.ModelSerializer):
    """Сериализатор моделей"""
    brand = BrandSerializer()
    class Meta:
        model = ProductModel
        fields = [
            'name', 'brand',
            'description'
        ]


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор продуктов"""
    model = ProductModelSerializer()
    class Meta:
        model = Product
        fields = [
            'gender', 'name',
            'description', 'attributes',
            'is_active', 'is_new', 'is_bestseller'
        ]


class ColorSerializer(serializers.ModelSerializer):
    """Сериализатор цвета"""
    class Meta:
        model = Color
        fields = [
            'name', 'hexcode'
        ]


class SizeSerializer(serializers.ModelSerializer):
    """Сериализатор размеров"""
    class Meta:
        model = Size
        fields = ['name']


class ProductVariantSerializer(serializers.ModelSerializer):
    """Сериализатор вариантов продукта"""
    color = ColorSerializer(read_only=True)
    size = SizeSerializer(read_only=True)

    color_id = serializers.PrimaryKeyRelatedField(
        queryset=Color.objects.all(), source='color', write_only=True)
    size_id = serializers.PrimaryKeyRelatedField(
        queryset=Size.objects.all(), source='size', write_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            'price', 'quantity', 'color',
            'size', 'color_id', 'size_id']


class ImageProductSerializer(serializers.ModelSerializer):
    """Сериализатор изображений"""
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True,
    )
    color = ColorSerializer(read_only=True)

    class Meta:
        model = ImageProduct
        fields = [
            'image', 'image_type', 'is_main',
            'order', 'product_id'
        ]


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов"""
    class Meta:
        model = Tag
        fields = ['name']


class TagToProductSerializer(serializers.ModelSerializer):
    """Сериализатор тегов продукта"""
    tag = TagSerializer()
    product = ProductSerializer()

    class Meta:
        model = TagToProduct
        fields = ['id', 'product', 'tag']



class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id', 'name',
            'image', 'slug'
        ]


class ProductListSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug',
        ]
    
    def get_main_image(self, obj):
        images = obj.images.filter(is_main=True).first()
        return images.image.url if images else None