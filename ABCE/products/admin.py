from django.contrib import admin
from django.db import models
from .models import (
    Category, Brand, ProductModel, Product, 
    Size, ProductVariant, ImageProduct, Tag, TagToProduct, Color)
from django.forms import widgets


class JSONFieldWidget(widgets.Textarea):
    def format_value(self, value):
        if value and isinstance(value, dict):
            import json
            return json.dumps(value, indent=2, ensure_ascii=False)
        return super().format_value(value)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['color', 'slug', 'hexcode']
    list_editable = ['slug', 'hexcode']
    search_fields = ['color']
    prepopulated_fields = {'slug': ('color',)}
    fieldsets = (
        ('Основное', {
            'fields': ('color', 'slug', 'hexcode')
        }),
    )

class ProductVariantInline(admin.TabularInline):
    """Инлайн для размеров товара"""
    model = ProductVariant
    extra = 1
    fields = ['size', 'price', 'quantity']
    autocomplete_fields = ['size']

class ImageProductInline(admin.TabularInline):
    """Инлайн для изображений товара"""
    model = ImageProduct
    extra = 1
    fields = ['image', 'image_type', 'is_main', 'order', 'color']
    autocomplete_fields = ['color']
    

class TagToProductInline(admin.TabularInline):
    """Инлайн для тегов товара"""
    model = TagToProduct
    extra = 1
    autocomplete_fields = ['tag']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'slug']
    list_filter = ['parent']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Основное', {
            'fields': ('name', 'slug', 'parent', 'image')
        }),
    )

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Основное', {
            'fields': ('name', 'slug', 'logo',)
        }),
    )

@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand']
    list_filter = ['brand']
    search_fields = ['name', 'brand__name']
    autocomplete_fields = ['brand']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Основное', {
            'fields': ('name', 'slug', 'brand', 'description')
        }),
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'brand', 'model', 
        'is_active', 'is_new', 'is_bestseller', 'gender'
    ]
    list_filter = ['category', 'brand', 'is_active', 'is_new', 'is_bestseller']
    search_fields = ['name', 'description']
    autocomplete_fields = ['category', 'brand', 'model']
    prepopulated_fields = {'slug': ('name',)}
    
    inlines = [ProductVariantInline, ImageProductInline, TagToProductInline]
    
    formfield_overrides = {
        models.JSONField: {'widget': JSONFieldWidget(attrs={'rows': 10})},
    }

    fieldsets = (
        ('Основное', {
            'fields': ('name', 'slug', 'description', 'gender')
        }),
        ('Связи', {
            'fields': ('category', 'brand', 'model')
        }),
        ('Статусы', {
            'fields': ('is_active', 'is_new', 'is_bestseller')
        }),
    )

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'price', 'quantity']
    list_filter = ['size']
    search_fields = ['product__name', 'size__name']
    autocomplete_fields = ['product', 'size']

@admin.register(ImageProduct)
class ImageProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_type', 'is_main', 'order', 'color']
    list_filter = ['image_type', 'is_main']
    search_fields = ['product__name']
    autocomplete_fields = ['product']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(TagToProduct)
class TagToProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'tag']
    list_filter = ['tag']
    search_fields = ['product__name', 'tag__name']
    autocomplete_fields = ['product', 'tag']