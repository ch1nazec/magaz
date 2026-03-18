from django.contrib import admin
from models import Cart, CartItem


# Register your models here.
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ['variant', 'quantity', 'total_price']
    readonly_fields = ['total_price']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'total_price']
    inlines = [CartItemInline]
    readonly_fields = ['total_price']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'variant', 'quantity', 'total_price']
    list_filter = ['cart']