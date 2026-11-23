from django.db import transaction
from django.db.models import F
from django.core.exceptions import ValidationError

from cart.models import Cart
from products.models import Stock
from .models import Order, OrderItem


@transaction.atomic
def create_order_from_cart(*, user, phone_number: str, address: str, comment: str = "") -> Order:
    try:
        cart = (
            Cart.objects
            .select_related("user")
            .prefetch_related("items__product", "items__warehouse")
            .get(user=user)
        )
    except Cart.DoesNotExist:
        raise ValidationError("Корзина не найдена")

    items = list(cart.items.select_related("product", "warehouse"))
    if not items:
        raise ValidationError("Корзина пуста")

    total = 0
    order_items_data = []

    # 1. Атомарно списываем остатки
    for item in items:
        updated = (
            Stock.objects
            .filter(
                product=item.product,
                warehouse=item.warehouse,
                quantity__gte=item.quantity
            )
            .update(quantity=F("quantity") - item.quantity)
        )

        if updated == 0:
            raise ValidationError(
                f"Недостаточно товара «{item.product.article}» "
                f"на складе {item.warehouse.city}"
            )

        total += item.price * item.quantity
        order_items_data.append(item)

    # 2. Создаём заказ
    order = Order.objects.create(
        user=user,
        phone_number=phone_number,
        address=address,
        comment=comment,
        total_amount=total,
        warehouse=order_items_data[0].warehouse,
        status="new",
    )

    # 3. Создаём позиции заказа (снимок данных)
    OrderItem.objects.bulk_create([
        OrderItem(
            order=order,
            product=item.product,
            warehouse=item.warehouse,
            article=item.product.article,
            product_name=item.product.name,
            warehouse_name=f"{item.warehouse.name} ({item.warehouse.city})",
            price=item.price,
            quantity=item.quantity,
        )
        for item in order_items_data
    ])

    # 4. Очищаем корзину
    cart.items.all().delete()

    return order