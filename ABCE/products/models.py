from django.db import models
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):
    """Категории товаров со вложенностью"""

    name = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='categories/', verbose_name='Изображение категории', blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Brand(models.Model):
    """Бренд производитель (Nike, Adidas...)"""
    name = models.CharField(max_length=100, blank=False, verbose_name='Название бренда')
    slug = models.SlugField(max_length=100, blank=True, unique=True)
    logo = models.ImageField(
        upload_to='brands/',
        verbose_name='Логотип бренда',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class ProductModel(models.Model):
    """Модели брендов (Air Max, Ja Morant)"""
    name = models.CharField(max_length=100, blank=False, verbose_name='Название модели')
    slug = models.SlugField(max_length=100, blank=False, unique=True)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='models',
        verbose_name='Бренд',
    )
    description = models.TextField(
        max_length=1000,
        verbose_name='Описание модели',
        blank=True,
    )

    class Meta:
        ordering = ['brand', 'name']
        unique_together = ['brand', 'name']
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f'{self.brand.name}-{self.name}')
            self.slug = base_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.brand.name} {self.name}'


class Product(models.Model):
    """Товар (без цены - цена в размерах)"""
    name = models.CharField(max_length=100, verbose_name='Название товара')
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(max_length=1000, verbose_name='Описание товара', blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория',
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Бренд',
    )
    model = models.ForeignKey(
        ProductModel,
        on_delete=models.SET_NULL,
        related_name='products',
        verbose_name='Модель',
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_new = models.BooleanField(default=False, verbose_name='Новинка')
    is_bestseller = models.BooleanField(default=False, verbose_name='Хит продаж')

    class Meta:
        ordering = ['name']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['brand']),
        ]

    def __str__(self):
        return self.name


class Size(models.Model):
    """Размеры (S, M, L, 42, 43 и т.д.)"""
    name = models.CharField(max_length=20, verbose_name='Размер модели')
    slug = models.SlugField(max_length=20, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductToSize(models.Model):
    """СВЯЗЬ ТОВАРА С РАЗМЕРОМ (здесь живет ЦЕНА и КОЛИЧЕСТВО)"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes', verbose_name='Товар')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='products', verbose_name='Размер')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена для этого товара'
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')

    class Meta:
        unique_together = ['product', 'size']
        verbose_name = 'Размер товара'
        verbose_name_plural = 'Размеры товаров'
    
    def __str__(self):
        return f"{self.product.name} - {self.size.name}: {self.price}₽"


class ImageProduct(models.Model):
    """Изображения товара"""
    IMAGE_TYPES = (
        ('main', 'Главное'),
        ('gallery', 'Галерея'),
        ('model', 'Модель')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Товар'
    )
    image = models.ImageField(
        upload_to='product/',
        verbose_name='Изображение'
    )
    image_type = models.CharField(
        max_length=10,
        choices=IMAGE_TYPES,
        default='gallery',
        verbose_name='Тип изображения',
    )
    is_main = models.BooleanField(default=False, verbose_name='Главное')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order', '-is_main']
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'

    def save(self, *args, **kwargs):
        if self.is_main:
            ImageProduct.objects.filter(
                product=self.product,
                is_main=True,
            ).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.product.name}'

class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название тега', unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class TagToProduct(models.Model):
    """Связь тегов и продуктов"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='tags', verbose_name='Продукт')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='products', verbose_name='Тег')

    class Meta:
        unique_together = ['product', 'tag']
        verbose_name = 'Тег товара'
        verbose_name_plural = 'Теги товаров'
    
    def __str__(self):
        return f'{self.product.name} - {self.tag.name}'