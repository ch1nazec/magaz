from django.db import models
from django.conf import settings

from django.core.exceptions import ValidationError
from products.models import Product, Warehouse, Stock


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения заказа')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
    
    def __str__(self):
        return f'Корзина юзера #{self.user.pk}'
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Товар'
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name='cart_items',
        verbose_name='Склад'
    )

    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Цена'
    )

    @property
    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f'{self.product.article} × {self.quantity} ({self.warehouse.city})'

    def clean(self):
        try:
            stock = Stock.objects.get(product=self.product, warehouse=self.warehouse)

            if self.quantity > stock.quantity:
                raise ValidationError(
                    f'Недостаточно товара. Доступно {stock.quantity} шт.'
                )
        except Stock.DoesNotExist:
            raise ValidationError('Товара нет на выбранном складе.')
    
    def save(self, *args, **kwargs):
        if self.quantity <= 0:
            if self.pk:
                self.delete()
            return

        if self.price is None or self.price == 0:
            stock = Stock.objects.filter(
                product=self.product,
                warehouse=self.warehouse,
            ).first()

            if not stock:
                raise ValidationError('Товар отсутствует на складе.')
            self.price = stock.price

        self.full_clean()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
        unique_together = ["cart", "product", "warehouse"]
        indexes = [
            models.Index(fields=["cart", "product", "warehouse"]),
        ]
    