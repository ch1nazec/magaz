from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from products.models import Product, Warehouse


class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "Новый"),
        ("processing", "В обработке"),
        ("shipped", "Отправлен"),
        ("delivered", "Доставлен"),
        ("cancelled", "Отменён"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="orders",
        verbose_name="Клиент"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
        verbose_name="Статус"
    )
    phone_number = models.CharField(
        max_length=25,
        verbose_name="Телефон",
        validators=[
            RegexValidator(
                regex=r"^(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$",
                message="Формат: +7 (999) 123-45-67 или 89991234567"
            )
        ]
    )
    address = models.TextField(max_length=500, verbose_name="Адрес доставки")
    comment = models.TextField(max_length=1000, blank=True, verbose_name="Комментарий")

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="Склад отгрузки"
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Сумма заказа"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Заказ"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Товар"
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Склад"
    )

    # Снимки на момент заказа
    article = models.CharField(max_length=9, verbose_name="Артикул")
    product_name = models.CharField(max_length=300, verbose_name="Название")
    warehouse_name = models.CharField(max_length=150, verbose_name="Склад")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(verbose_name="Количество")

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self):
        return f"{self.article} × {self.quantity}"

    @property
    def total_price(self):
        return self.price * self.quantity