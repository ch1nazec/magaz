import secrets

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, action, permission_classes

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import F
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

from functools import wraps

from .models import Order, OrderItem
from .serializer import OrderSerializer, CreateOrderSerializer
from .permissions import IsAdminOrBot

from cart.models import Cart, CartItem
from django.core.cache import cache
from products.models import Stock
from rest_framework import mixins

from others.decorators import auto_clear_cache, auto_set_cache
from others.delete_cache import delete_cache


def invalidate_order_cache(user_id: int):
    cache.delete(f"order:user:{user_id}")

#Декораторы

def admin_bot_check(func):
    @wraps(func)
    def wrapper(request: Request, *args, **kwargs):
        is_admin = bool(request.user and request.user.is_authenticated and request.user.is_staff)
        
        incoming_token = request.headers.get("X-Bot-Token", "")
        expected_token = getattr(settings, "BOT_API", "") or ""
        
        # Сравниваем безопасно и только если токен реально задан в настройках
        is_bot = bool(expected_token) and secrets.compare_digest(incoming_token, expected_token)

        if not (is_admin or is_bot):
            return Response(
                {"message": "Только администраторы могут сделать это"},
                status=status.HTTP_403_FORBIDDEN
            )
        return func(request, *args, **kwargs)
    return wrapper


def order_cancel_check(func):
    @wraps(func)
    def wrapper(request: Request, *args, **kwargs):
        order = kwargs.get("order")
        if order and order.status == "cancelled":
            return Response(
                {"message": "Заказ уже отменён!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return func(request, *args, **kwargs)
    return wrapper


def order_exists(func):
    @wraps(func)
    def wrapper(request: Request, *args, **kwargs):
        order_id = kwargs.get("order_id")
        if not order_id:
            return Response(
                {"message": "Заказ не указан"},
                status=status.HTTP_400_BAD_REQUEST
            )
        order = get_object_or_404(Order, pk=order_id)
        kwargs["order"] = order
        return func(request, *args, **kwargs)
    return wrapper


# ====================== ViewSet ======================

@auto_clear_cache()
@auto_set_cache(pattern="user_")
class OrderViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "phone_number"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.prefetch_related("items").all()
        
        data = Order.objects.filter(user=user).prefetch_related("items")
        return data


    def list(self, request, *args, **kwargs):
        user = request.user

        if user.is_staff or request.query_params:
            return super().list(request, *args, **kwargs)

        cache_key = f'order:user:{user.id}'
        data = cache.get(cache_key)

        if data is not None:
            return Response(data)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        cache.set(cache_key, data, timeout=60 * 5)
        return Response(data)


    def create(self, request: Request):
        """
        Создание заказа из корзины (БД-корзина).
        POST /api/orders/
        {
            "phone_number": "+79991234567",
            "address": "Уссурийск, ...",
            "comment": "..."
        }
        """
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        phone = serializer.validated_data["phone_number"]
        address = serializer.validated_data["address"]
        comment = serializer.validated_data.get("comment", "")

        try:
            with transaction.atomic():
                cart = (
                    Cart.objects
                    .select_related("user")
                    .prefetch_related("items__product", "items__warehouse")
                    .get(user=user)
                )

                items = list(cart.items.select_related("product", "warehouse"))
                if not items:
                    return Response(
                        {"error": "Корзина пуста"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                total_amount = 0
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
                        # Откатываем всю транзакцию
                        raise ValidationError(
                            f"Недостаточно товара «{item.product.article}» "
                            f"на складе {item.warehouse.city}"
                        )

                    total_amount += item.price * item.quantity
                    order_items_data.append(item)

                # 2. Создаём заказ
                order = Order.objects.create(
                    user=user,
                    phone_number=phone,
                    address=address,
                    comment=comment,
                    total_amount=total_amount,
                    warehouse=order_items_data[0].warehouse,
                    status="new",
                )

                # 3. Создаём позиции (снимок данных)
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

        except Cart.DoesNotExist:
            return Response(
                {"error": "Корзина не найдена"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationError as e:
            return Response(
                {"error": str(e.message) if hasattr(e, "message") else str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        invalidate_order_cache(user.id)
        # delete_cache("order_list_*")
        
        return Response(
            OrderSerializer(order, context={"request": request}).data,
            status=status.HTTP_201_CREATED
        )


# ====================== Дополнительные эндпоинты ======================

@api_view(["GET"])
@permission_classes([IsAdminOrBot])
@order_exists
def order_get(request: Request, order_id: int, order: Order = None):
    return Response(OrderSerializer(order).data)


@api_view(["PATCH"])
@permission_classes([IsAdminOrBot])
@order_exists
@order_cancel_check
def cancel_order(request: Request, order_id: int, order: Order = None) -> Response:
    """
    Отмена заказа + возврат товара на склад
    """
    with transaction.atomic():
        order = get_object_or_404(Order.objects.select_for_update(), pk=order_id)
        if order.status == "cancelled":
            return Response(
                {"message": "Заказ уже отменён!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        
        for item in order.items.select_related("product", "warehouse"):
            if item.product and item.warehouse:
                Stock.objects.filter(
                    product=item.product,
                    warehouse=item.warehouse
                ).update(quantity=F("quantity") + item.quantity)

        order.status = "cancelled"
        order.save(update_fields=["status"])


    if order.user_id:
        invalidate_order_cache(order.user_id)
    # delete_cache("order_list_*")
    return Response({"message": f"Успешно отменён заказ #{order.pk}!"})


@api_view(["PATCH"])
@permission_classes([IsAdminOrBot])
@order_exists
@order_cancel_check
def sent_order(request: Request, order_id: int, order: Order = None) -> Response:
    if order.status == "shipped":
        return Response(
            {"message": "Заказ уже отправлен."},
            status=status.HTTP_400_BAD_REQUEST
        )

    order.status = "shipped"
    order.save(update_fields=["status"])

    # delete_cache("order_list_*")
    if order.user_id:
        invalidate_order_cache(order.user_id)
    return Response({"message": "Заказ отправлен!"}, status=status.HTTP_202_ACCEPTED)


@api_view(["PATCH"])
@permission_classes([IsAdminOrBot])
@order_exists
@order_cancel_check
def confirm_order(request: Request, order_id: int, order: Order = None) -> Response:
    if order.status == 'delivered':
        return Response({'message': 'Заказ уже доставлен.'}, status=status.HTTP_400_BAD_REQUEST)

    order.status = "delivered"
    order.save(update_fields=["status"])

    # delete_cache("order_list_*")
    if order.user_id:
        invalidate_order_cache(order.user_id)
    return Response({"message": "Заказ успешно доставлен!"}, status=status.HTTP_202_ACCEPTED)