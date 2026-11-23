from django.db import models
from django.utils.text import slugify
from django.core.validators import RegexValidator
from mptt.models import MPTTModel, TreeForeignKey


# 1. Категории (дерево)
class Category(MPTTModel):
    """Каталог товаров (меню)"""
    name = models.CharField("Название", max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    image = models.ImageField("Изображение", upload_to="categories/", blank=True, null=True)
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Родительская категория"
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# 2. Бренды запчастей
class Brand(models.Model):
    """Производители запчастей"""
    name = models.CharField("Название", max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    logo = models.ImageField("Логотип", upload_to="brands/", blank=True, null=True)

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# 3. Автомобили (иерархия)
class VehicleMake(models.Model):
    """Марка: Toyota, BMW, Hyundai..."""
    name = models.CharField("Марка", max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    logo = models.ImageField("Логотип", upload_to="makes/", blank=True, null=True)

    class Meta:
        verbose_name = "Марка автомобиля"
        verbose_name_plural = "Марки автомобилей"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class VehicleModel(models.Model):
    """Модель: Camry, X5, Tucson..."""
    make = models.ForeignKey(VehicleMake, on_delete=models.CASCADE, related_name="models")
    name = models.CharField("Модель", max_length=100)
    slug = models.SlugField(max_length=150, blank=True)

    class Meta:
        verbose_name = "Модель автомобиля"
        verbose_name_plural = "Модели автомобилей"
        unique_together = ["make", "name"]
        ordering = ["make__name", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.make.name}-{self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.make.name} {self.name}"

class VehicleGeneration(models.Model):
    """Поколение: XV70 (2017-2024), F15 и т.д."""
    model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE, related_name="generations")
    name = models.CharField("Название поколения", max_length=100, blank=True)
    year_from = models.PositiveSmallIntegerField("Год начала")
    year_to = models.PositiveSmallIntegerField("Год окончания", null=True, blank=True)
    body = models.CharField("Кузов", max_length=50, blank=True)  # sedan, SUV...

    class Meta:
        verbose_name = "Поколение"
        verbose_name_plural = "Поколения"
        ordering = ["model", "-year_from"]

    def __str__(self):
        years = f"{self.year_from}" + (f"–{self.year_to}" if self.year_to else "+")
        return f"{self.model} {self.name} ({years})".strip()

class VehicleModification(models.Model):
    """Конкретная модификация: 2.5 AT, 3.0d xDrive и т.д."""
    generation = models.ForeignKey(VehicleGeneration, on_delete=models.CASCADE, related_name="modifications")
    name = models.CharField("Название модификации", max_length=150)
    engine_code = models.CharField("Код двигателя", max_length=50, blank=True)
    engine_volume = models.CharField("Объём", max_length=20, blank=True)
    fuel = models.CharField("Топливо", max_length=30, blank=True)          # petrol / diesel / hybrid
    transmission = models.CharField("КПП", max_length=50, blank=True)
    drive = models.CharField("Привод", max_length=20, blank=True)           # FWD / RWD / AWD
    year_from = models.PositiveSmallIntegerField(null=True, blank=True)
    year_to = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Модификация"
        verbose_name_plural = "Модификации"
        ordering = ["generation", "name"]

    def __str__(self):
        return f"{self.generation} → {self.name}"


# 4. Товар (Product)
class Product(models.Model):
    # Внутренний артикул магазина: 000000001, 000000002...
    article = models.CharField(
        "Внутренний артикул",
        max_length=9,
        unique=True,
        validators=[RegexValidator(r"^\d{9}$", "Артикул должен состоять из 9 цифр")]
    )
    name = models.CharField("Название", max_length=300)
    slug = models.SlugField(max_length=320, unique=True, blank=True)
    description = models.TextField("Описание", blank=True)
    attributes = models.JSONField("Характеристики", default=dict, blank=True)

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="products")

    is_active = models.BooleanField("Активен", default=True)
    is_new = models.BooleanField("Новинка", default=False)
    is_bestseller = models.BooleanField("Хит продаж", default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["article"]),
            models.Index(fields=["is_active", "category"]),
            models.Index(fields=["brand"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.article}-{self.name}")[:320]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.article}] {self.name}"

def get_next_article() -> str:
    """Генерирует следующий артикул вида 000000001"""
    last = Product.objects.order_by("-article").values_list("article", flat=True).first()
    next_num = int(last) + 1 if last else 1
    return f"{next_num:09d}"


# 5. Внешние артикулы (OEM + кроссы)
class ProductArticle(models.Model):
    TYPE_CHOICES = [
        ("oem", "Оригинал (OEM)"),
        ("aftermarket", "Aftermarket"),
        ("cross", "Кросс / аналог"),
        ("other", "Другое"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="articles")
    number = models.CharField("Номер", max_length=60, db_index=True)
    type = models.CharField("Тип", max_length=20, choices=TYPE_CHOICES, default="oem")
    brand_name = models.CharField("Бренд номера", max_length=100, blank=True)  # Toyota, Bosch...
    is_main = models.BooleanField("Основной", default=False)

    class Meta:
        verbose_name = "Артикул / кросс"
        verbose_name_plural = "Артикулы и кроссы"
        unique_together = ["product", "number"]
        indexes = [
            models.Index(fields=["number"]),
        ]

    def __str__(self):
        return f"{self.number} ({self.get_type_display()})"


# 6. Применяемость
class PartApplicability(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="applicabilities")
    modification = models.ForeignKey(VehicleModification, on_delete=models.CASCADE, related_name="parts")
    note = models.CharField("Примечание", max_length=200, blank=True)  # передний левый, с АБС и т.д.
    is_confirmed = models.BooleanField("Подтверждено", default=True)

    class Meta:
        verbose_name = "Применяемость"
        verbose_name_plural = "Применяемость"
        unique_together = ["product", "modification"]

    def __str__(self):
        return f"{self.product.article} → {self.modification}"


# 7. Изображения
class ProductImage(models.Model):
    IMAGE_TYPES = (
        ("main", "Главное"),
        ("gallery", "Галерея"),
        ("scheme", "Схема"),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/")
    image_type = models.CharField(max_length=10, choices=IMAGE_TYPES, default="gallery")
    is_main = models.BooleanField("Главное", default=False)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"
        ordering = ["order", "-is_main"]

    def save(self, *args, **kwargs):
        if self.is_main:
            ProductImage.objects.filter(product=self.product, is_main=True).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Изображение {self.product.article}"

# 8. Склады и остатки 
class Warehouse(models.Model):
    name = models.CharField("Название склада", max_length=100)
    city = models.CharField("Город", max_length=100, db_index=True)
    address = models.CharField("Адрес", max_length=255, blank=True)
    is_active = models.BooleanField("Активен", default=True)
    sort_order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"
        ordering = ["sort_order", "city", "name"]

    def __str__(self):
        return f"{self.name} ({self.city})"

class Stock(models.Model):
    """
    Здесь хранится ВСЁ, что зависит от склада:
    - количество
    - цена
    - старая цена (для скидки)
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stocks")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="stocks")

    quantity = models.PositiveIntegerField("Количество", default=0)
    price = models.DecimalField("Цена", max_digits=12, decimal_places=2)
    price_old = models.DecimalField("Старая цена", max_digits=12, decimal_places=2, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Остаток на складе"
        verbose_name_plural = "Остатки на складах"
        unique_together = ["product", "warehouse"]
        indexes = [
            models.Index(fields=["warehouse", "quantity"]),
            models.Index(fields=["product", "warehouse"]),
        ]

    def __str__(self):
        return f"{self.product.article} | {self.warehouse.city}: {self.quantity} шт. — {self.price} ₽"