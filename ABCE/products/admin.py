from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from .models import (
    Category, Brand,
    VehicleMake, VehicleModel, VehicleGeneration, VehicleModification,
    Product, ProductArticle, PartApplicability, ProductImage,
    Warehouse, Stock,
)


# ---------- Категории ----------
@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ("tree_actions", "indented_title", "slug", "image_tag")
    list_display_links = ("indented_title",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description="Изображение")
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;" />', obj.image.url)
        return "—"


# ---------- Бренды ----------
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "logo_tag")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description="Логотип")
    def logo_tag(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:30px;" />', obj.logo.url)
        return "—"


# ---------- Автомобили ----------
@admin.register(VehicleMake)
class VehicleMakeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "logo_tag")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description="Логотип")
    def logo_tag(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:30px;" />', obj.logo.url)
        return "—"


@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    list_display = ("name", "make", "slug")
    list_filter = ("make",)
    search_fields = ("name", "make__name")
    autocomplete_fields = ("make",)
    prepopulated_fields = {"slug": ("make", "name")}  # если нужно — можно убрать


@admin.register(VehicleGeneration)
class VehicleGenerationAdmin(admin.ModelAdmin):
    list_display = ("__str__", "model", "year_from", "year_to", "body")
    list_filter = ("model__make", "body")
    search_fields = ("name", "model__name", "model__make__name")
    autocomplete_fields = ("model",)


@admin.register(VehicleModification)
class VehicleModificationAdmin(admin.ModelAdmin):
    list_display = ("__str__", "generation", "engine_code", "engine_volume",
                    "fuel", "transmission", "drive", "year_from", "year_to")
    list_filter = ("fuel", "drive", "transmission")
    search_fields = ("name", "engine_code", "generation__model__name",
                     "generation__model__make__name")
    autocomplete_fields = ("generation",)


# ---------- Товары ----------
class ProductArticleInline(admin.TabularInline):
    model = ProductArticle
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "image_type", "is_main", "order")


class PartApplicabilityInline(admin.TabularInline):
    model = PartApplicability
    extra = 0
    autocomplete_fields = ("modification",)
    fields = ("modification", "note", "is_confirmed")


class StockInline(admin.TabularInline):
    model = Stock
    extra = 0
    autocomplete_fields = ("warehouse",)
    fields = ("warehouse", "quantity", "price", "price_old", "updated_at")
    readonly_fields = ("updated_at",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("article", "name", "brand", "category",
                    "is_active", "is_new", "is_bestseller", "created_at")
    list_filter = ("is_active", "is_new", "is_bestseller", "brand", "category")
    search_fields = ("article", "name", "brand__name", "category__name")
    prepopulated_fields = {"slug": ("article", "name")}
    autocomplete_fields = ("category", "brand")
    date_hierarchy = "created_at"
    inlines = [ProductArticleInline, ProductImageInline,
               PartApplicabilityInline, StockInline]
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("article", "name", "slug", "description")}),
        ("Классификация", {"fields": ("category", "brand")}),
        ("Флаги", {"fields": ("is_active", "is_new", "is_bestseller")}),
        ("Характеристики", {"fields": ("attributes",)}),
        ("Служебное", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(ProductArticle)
class ProductArticleAdmin(admin.ModelAdmin):
    list_display = ("number", "product", "type", "brand_name", "is_main")
    list_filter = ("type", "is_main")
    search_fields = ("number", "brand_name", "product__article", "product__name")
    autocomplete_fields = ("product",)


@admin.register(PartApplicability)
class PartApplicabilityAdmin(admin.ModelAdmin):
    list_display = ("product", "modification", "note", "is_confirmed")
    list_filter = ("is_confirmed",)
    search_fields = ("product__article", "product__name", "modification__name")
    autocomplete_fields = ("product", "modification")


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "image_tag", "image_type", "is_main", "order")
    list_filter = ("image_type", "is_main")
    search_fields = ("product__article", "product__name")
    autocomplete_fields = ("product",)
    ordering = ("product", "order")

    @admin.display(description="Превью")
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;" />', obj.image.url)
        return "—"


# ---------- Склады и остатки ----------
@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "address", "is_active", "sort_order")
    list_filter = ("is_active", "city")
    search_fields = ("name", "city", "address")
    ordering = ("sort_order", "city", "name")


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("product", "warehouse", "quantity", "price", "price_old", "updated_at")
    list_filter = ("warehouse",)
    search_fields = ("product__article", "product__name", "warehouse__name")
    autocomplete_fields = ("product", "warehouse")
    readonly_fields = ("updated_at",)
    list_select_related = ("product", "warehouse")