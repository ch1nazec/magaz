from django.contrib import admin
from django.utils.html import format_html

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ("product", "warehouse", "article", "product_name",
              "warehouse_name", "price", "quantity", "total_price_display")
    readonly_fields = ("article", "product_name", "warehouse_name",
                       "price", "quantity", "total_price_display")
    autocomplete_fields = ("product", "warehouse")
    can_delete = False

    @admin.display(description="Сумма")
    def total_price_display(self, obj):
        return obj.total_price if obj.pk else "—"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "phone_number",
                    "warehouse", "total_amount", "created_at")
    list_filter = ("status", "warehouse", "created_at")
    search_fields = ("id", "phone_number", "address",
                     "user__email", "user__phone_number")
    autocomplete_fields = ("user", "warehouse")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at", "total_amount")
    inlines = [OrderItemInline]
    list_select_related = ("user", "warehouse")
    fieldsets = (
        ("Клиент", {"fields": ("user", "phone_number", "address", "comment")}),
        ("Доставка", {"fields": ("warehouse", "status")}),
        ("Сумма", {"fields": ("total_amount",)}),
        ("Служебное", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "article", "product_name",
                    "warehouse_name", "price", "quantity", "total_price")
    list_filter = ("warehouse",)
    search_fields = ("article", "product_name", "order__id", "order__phone_number")
    autocomplete_fields = ("order", "product", "warehouse")
    readonly_fields = ("order", "product", "warehouse",
                       "article", "product_name", "warehouse_name",
                       "price", "quantity") 