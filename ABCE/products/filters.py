import django_filters
from django.db.models import Q
from .models import Product, Stock

class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug")
    brand = django_filters.CharFilter(field_name="brand__slug")
    article = django_filters.CharFilter(lookup_expr="icontains")
    is_new = django_filters.BooleanFilter()
    is_bestseller = django_filters.BooleanFilter()
    is_active = django_filters.BooleanFilter()

    # Поиск по любому внешнему номеру
    number = django_filters.CharFilter(method="filter_number")

    # По модификации автомобиля
    modification = django_filters.NumberFilter(field_name="applicabilities__modification_id")

    # Наличие на конкретном складе / в городе
    warehouse = django_filters.NumberFilter(method="filter_warehouse")
    city = django_filters.CharFilter(method="filter_city")

    min_price = django_filters.NumberFilter(method="filter_min_price")
    max_price = django_filters.NumberFilter(method="filter_max_price")

    class Meta:
        model = Product
        fields = ["category", "brand", "article", "is_new", "is_bestseller", "is_active"]

    def filter_number(self, queryset, name, value):
        return queryset.filter(articles__number__icontains=value).distinct()

    def filter_warehouse(self, queryset, name, value):
        return queryset.filter(
            stocks__warehouse_id=value,
            stocks__quantity__gt=0
        ).distinct()

    def filter_city(self, queryset, name, value):
        return queryset.filter(
            stocks__warehouse__city__iexact=value,
            stocks__quantity__gt=0
        ).distinct()

    def filter_min_price(self, queryset, name, value):
        warehouse = self.data.get("warehouse")
        city = self.data.get("city")
        q = Q(stocks__price__gte=value)
        if warehouse:
            q &= Q(stocks__warehouse_id=warehouse)
        if city:
            q &= Q(stocks__warehouse__city__iexact=city)
        return queryset.filter(q).distinct()

    def filter_max_price(self, queryset, name, value):
        warehouse = self.data.get("warehouse")
        city = self.data.get("city")
        q = Q(stocks__price__lte=value)
        if warehouse:
            q &= Q(stocks__warehouse_id=warehouse)
        if city:
            q &= Q(stocks__warehouse__city__iexact=city)
        return queryset.filter(q).distinct()

class StockFilter(django_filters.FilterSet):
    warehouse = django_filters.NumberFilter(field_name="warehouse_id")
    city = django_filters.CharFilter(field_name="warehouse__city", lookup_expr="iexact")
    product = django_filters.NumberFilter(field_name="product_id")
    article = django_filters.CharFilter(field_name="product__article", lookup_expr="icontains")
    in_stock = django_filters.BooleanFilter(method="filter_in_stock")
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Stock
        fields = ["warehouse", "city", "product", "article"]

    def filter_in_stock(self, queryset, name, value):
        if value is True:
            return queryset.filter(quantity__gt=0)
        if value is False:
            return queryset.filter(quantity=0)
        return queryset