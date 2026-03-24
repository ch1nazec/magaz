from django_filters import NumberFilter
import django_filters
from products.models import ProductVariant


class ProductFilter(django_filters.FilterSet):
    min_price = NumberFilter(field_name='variants__price', lookup_expr='gte')
    max_price = NumberFilter(field_name='variants__price', lookup_expr='lte')

    class Meta:
        model = ProductVariant
        fields = ['gender', 'category_id', 'brand', 'is_active', 'min_price', 'max_price']