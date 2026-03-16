from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=100, unique=True)
    img = models.ImageField(upload_to='category/', verbose_name='Изображение категории')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название товара')
    description = models.TextField(max_length=1000, verbose_name='Описание товара')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='category'
    )


class ImageProduct(models.Model):
    IMAGE_TYPES = (
        ('product', 'Product'),
    )