from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import Cart, CartItem
from .serializer import CartSerializer, CartItemSerializer
from products.models import Stock

from django.core.cache import cache


def invalidate_cart_cache(user_id: int):
    cache.delete(f"cart:user:{user_id}")


class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_cart(self):
        cart, _ = Cart.objects.select_related("user").get_or_create(user=self.request.user)
        return cart

    def get_serialized_cart(self, cart, request):
        fresh_cart = (
            Cart.objects
            .prefetch_related("items__product", "items__warehouse")
            .get(pk=cart.pk)
        )
        return CartSerializer(fresh_cart, context={"request": request}).data


    def list(self, request):
        user_id = request.user.id
        cache_key = f'cart:user:{user_id}'

        data = cache.get(cache_key)
        if data is not None:
            return Response(data)

        cart = self.get_cart()
        
        data = self.get_serialized_cart(cart, request)
        cache.set(cache_key, data, timeout=30)
    
        return Response(data)

    @action(detail=False, methods=["post"], url_path="add")
    def add_item(self, request):
        user_id = request.user.id
        """
        POST /api/cart/add/
        {
            "product_id": 15,
            "warehouse_id": 2,
            "quantity": 1
        }
        """

        serializer = CartItemSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data["product"]
        warehouse = serializer.validated_data["warehouse"]
        quantity = serializer.validated_data.get("quantity", 1)

        cart = self.get_cart()

        if quantity <= 0:
            return Response({"detail": "Количество должно быть больше нуля"}, status=400)

        try:
            with transaction.atomic():
                # Блокируем строку остатка
                stock = Stock.objects.select_for_update().get(
                    product=product,
                    warehouse=warehouse
                )

                item = (
                    CartItem.objects
                    .select_for_update()
                    .filter(cart=cart, product=product, warehouse=warehouse)
                    .first()
                )

                new_quantity = quantity if not item else item.quantity + quantity

                if new_quantity > stock.quantity:
                    return Response(
                        {"detail": f"Недостаточно товара. Доступно: {stock.quantity} шт."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if item:
                    item.quantity = new_quantity
                    item.price = stock.price
                    item.save(update_fields=["quantity", "price"])
                    created = False
                else:
                    CartItem.objects.create(
                        cart=cart,
                        product=product,
                        warehouse=warehouse,
                        quantity=quantity,
                        price=stock.price
                    )
                    created = True

        except Stock.DoesNotExist:
            return Response(
                {"detail": "Товар отсутствует на выбранном складе"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart.refresh_from_db()

        invalidate_cart_cache(user_id)
        return Response(
            self.get_serialized_cart(cart, request),
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    @action(detail=False, methods=["patch"], url_path="update-item")
    def update_item(self, request):
        """
        PATCH /api/cart/update-item/
        {
            "item_id": 42,
            "quantity": 3
        }
        """
        user_id = request.user.id

        try:
            item_id = int(request.data.get("item_id"))
            quantity = int(request.data.get("quantity"))
        except (TypeError, ValueError):
            return Response(
                {"detail": "Параметры item_id и quantity должны быть целыми числами"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not item_id or quantity is None:
            return Response(
                {"detail": "Нужны item_id и quantity"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart = self.get_cart()
        item = get_object_or_404(CartItem, id=item_id, cart=cart)

        if quantity <= 0:
            item.delete()
            cart.refresh_from_db()
            invalidate_cart_cache(user_id)
            return Response(self.get_serialized_cart(cart, request))

        try:
            with transaction.atomic():
                stock = Stock.objects.select_for_update().get(
                    product=item.product,
                    warehouse=item.warehouse
                )

                if quantity > stock.quantity:
                    return Response(
                        {"detail": f"Недостаточно товара. Доступно: {stock.quantity} шт."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                item.quantity = quantity
                item.price = stock.price
                item.save(update_fields=["quantity", "price"])

        except Stock.DoesNotExist:
            return Response(
                {"detail": "Товар больше недоступен на этом складе"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart.refresh_from_db()
        invalidate_cart_cache(user_id)

        return Response(self.get_serialized_cart(cart, request))

    @action(detail=False, methods=["delete"], url_path="remove-item")
    def remove_item(self, request):
        user_id = request.user.id

        try:
            item_id = int(request.data.get("item_id"))
        except (TypeError, ValueError):
            return Response(
                {"detail": "Параметр item_id должен быть целым числом"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart = self.get_cart()
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()

        invalidate_cart_cache(user_id)
        return Response(self.get_serialized_cart(cart, request))

    @action(detail=False, methods=["delete"], url_path="clear")
    def clear(self, request):
        user_id = request.user.id

        cart = self.get_cart()
        cart.items.all().delete()
        
        invalidate_cart_cache(user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)