from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    autocomplete_fields = ("product", "warehouse")
    fields = ("product", "warehouse", "quantity", "price", "total_price_display")
    readonly_fields = ("total_price_display",)

    @admin.display(description="Сумма")
    def total_price_display(self, obj):
        return obj.total_price if obj.pk else "—"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_items_display", "total_price_display",
                    "created_at", "updated_at")
    search_fields = ("user__email", "user__username", "user__phone_number")
    autocomplete_fields = ("user",)
    readonly_fields = ("created_at", "updated_at",
                       "total_items_display", "total_price_display")
    inlines = [CartItemInline]
    list_select_related = ("user",)

    @admin.display(description="Товаров")
    def total_items_display(self, obj):
        return obj.total_items

    @admin.display(description="Сумма")
    def total_price_display(self, obj):
        return obj.total_price


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "warehouse",
                    "quantity", "price", "total_price_display")
    list_filter = ("warehouse",)
    search_fields = ("product__article", "product__name",
                     "cart__user__email", "cart__user__phone_number")
    autocomplete_fields = ("cart", "product", "warehouse")

    @admin.display(description="Сумма")
    def total_price_display(self, obj):
        return obj.total_price