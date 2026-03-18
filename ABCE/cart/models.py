from django.db import models
from django.conf import settings


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


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    variant = models.ForeignKey(
        'products.ProductVariant',
        on_delete=models.CASCADE,
        verbose_name='Вариант товара'
    )

    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    @property
    def total_price(self):
        return self.quantity * self.variant.price

    def __str__(self):
        return f'{self.variant.product.name} - {self.quantity} шт.'
    
    def save(self, *args, **kwargs):
        if self.quantity <= 0:
            self.delete()
            return
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
        unique_together = ['cart', 'variant']