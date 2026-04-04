from rest_framework import serializers
from .models import (Category, Brand, ProductModel,
                     Product, Color, Size,
                     ProductVariant, ImageProduct, Tag,
                     TagToProduct)


def check_name(name, value):
    """Проверка название без цифр"""
    if value.isalpha():
            return value
    else:
        raise serializers.ValidationError(f'{name} не может называться цифрами.')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""
    children = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'image', 'image_url',
            'parent', 'children'
        ]
    
    def validate_name(self, value: str) -> str:
        return check_name(name='Категория', value=value)
    
    def get_children(self, obj):
        children = obj.children.all()
        if children:
            return CategorySerializer(obj.children.all(), many=True).data
        return []
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url') and request:
            return request.build_absolute_uri(obj.image.url)
        return
    

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
    product_model  = ProductModelSerializer(source='model', read_only=True)
    class Meta:
        model = Product
        fields = [ 'id',
            'gender', 'name',
            'description', 'attributes',
            'is_active', 'is_new', 'is_bestseller', 'product_model',
            'slug', 'category_id', 'brand_id'
        ]
    


class ColorSerializer(serializers.ModelSerializer):
    """Сериализатор цвета"""
    class Meta:
        model = Color
        fields = [
            "id", 'color', 'hexcode', 'slug'
        ]


class SizeSerializer(serializers.ModelSerializer):
    """Сериализатор размеров"""
    class Meta:
        model = Size
        fields = ["id", 'name']


class ProductVariantSerializer(serializers.ModelSerializer):
    """Сериализатор вариантов продукта"""
    product = ProductSerializer()
    product_id = serializers.SerializerMethodField()

    color = ColorSerializer(read_only=True)
    size = SizeSerializer(read_only=True)

    color_id = serializers.PrimaryKeyRelatedField(
        queryset=Color.objects.all(), source='color', write_only=True)
    size_id = serializers.PrimaryKeyRelatedField(
        queryset=Size.objects.all(), source='size', write_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            'id', 'product_id', 'product',
            'price', 'quantity', 'color',
            'size', 'color_id', 'size_id']
    def get_product_id(self, obj):
        return obj.product.id


class ImageProductSerializer(serializers.ModelSerializer):
    """Сериализатор изображений"""
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True,
    )
    color = ColorSerializer(read_only=True)

    class Meta:
        model = ImageProduct
        fields = [
            "id", 'product_id', 'image', 'color', 'image_type', 'is_main',
            'order', 
        ]


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов"""
    class Meta:
        model = Tag
        fields = ["id", 'name', "slug"]


class TagToProductSerializer(serializers.ModelSerializer):
    tag_id = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), source='tag', write_only=True
    )
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    tag = TagSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = TagToProduct
        fields = ['id', 'tag', 'product', 'tag_id', 'product_id']



class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id', 'name',
            'image', 'slug'
        ]
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)


class ProductListSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug',
            'is_active', 'is_new', 'is_bestseller'
        ]
    
    def get_main_image(self, obj):
        images = obj.images.filter(is_main=True).first()
        return images.image.url if images else None