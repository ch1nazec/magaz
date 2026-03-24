from django_filters import NumberFilter, CharFilter, BooleanFilter
import django_filters
from products.models import ProductVariant


class ProductVariantFilter(django_filters.FilterSet):
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')

    min_quantity = NumberFilter(field_name='quantity', lookup_expr='gte')
    gender = CharFilter(field_name='product__gender')
    name = CharFilter(field_name='product__name', lookup_expr='icontains')

    is_active = BooleanFilter(field_name='product__is_active')
    is_new = BooleanFilter(field_name='product__is_new')
    is_bestseller = BooleanFilter(field_name='product__is_bestseller')

    product_model = CharFilter(field_name='product__product_model__name')
    brand = CharFilter(field_name='brand_id')
    
    color = CharFilter(field_name='color__color')
    size = CharFilter(field_name='size__name')


    class Meta:
        model = ProductVariant
        fields = ['min_price', 'max_price']