from django.contrib import admin
from .models import (
    Category, Brand, ProductModel, Product, 
    Size, ProductToSize, ImageProduct, Tag, TagToProduct
)

class ProductToSizeInline(admin.TabularInline):
    """Инлайн для размеров товара"""
    model = ProductToSize
    extra = 1
    fields = ['size', 'price', 'quantity']
    autocomplete_fields = ['size']

class ImageProductInline(admin.TabularInline):
    """Инлайн для изображений товара"""
    model = ImageProduct
    extra = 1
    fields = ['image', 'image_type', 'is_main', 'order']

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
        'is_active', 'is_new', 'is_bestseller'
    ]
    list_filter = ['category', 'brand', 'is_active', 'is_new', 'is_bestseller']
    search_fields = ['name', 'description']
    autocomplete_fields = ['category', 'brand', 'model']
    prepopulated_fields = {'slug': ('name',)}
    
    inlines = [ProductToSizeInline, ImageProductInline, TagToProductInline]
    
    fieldsets = (
        ('Основное', {
            'fields': ('name', 'slug', 'description')
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

@admin.register(ProductToSize)
class ProductToSizeAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'price', 'quantity']
    list_filter = ['size']
    search_fields = ['product__name', 'size__name']
    autocomplete_fields = ['product', 'size']

@admin.register(ImageProduct)
class ImageProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_type', 'is_main', 'order']
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