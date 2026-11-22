from django.db import models
from django.core.validators import RegexValidator
from user.models import CustomUser
from products.models import ProductVariant


# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]
    user = models.ForeignKey(
        CustomUser,
        related_name='orders',
        verbose_name='Клиент',
        on_delete=models.SET_NULL,
        null=True,
    )
    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default='новый'
    )
    comment = models.TextField(
        max_length=1_000,
        verbose_name='Комментарий к заказу',
        blank=True, null=True,
    )

    phone_regex = RegexValidator(
        regex=r'^(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$',
        message="Номер должен быть в формате: +7 (999) 123-45-67 или 89991234567"
    )
    phone_number = models.CharField(
        max_length=16,
        verbose_name='Номер телефона',
        validators=[phone_regex],
    )
    address = models.TextField(max_length=500, verbose_name='Адрес доставки',)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Закакз #{self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.CharField(max_length=200, verbose_name='Название')
    color = models.CharField(max_length=100, verbose_name='Цвет товара')
    size = models.CharField(max_length=20, verbose_name='Размер')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена товара'
    )
    quantity = models.PositiveIntegerField(verbose_name='Количество')