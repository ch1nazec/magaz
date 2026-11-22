from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework.permissions import AllowAny

from rest_framework.decorators import api_view
from django.conf import settings

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db import transaction
from others.decorators import auto_clear_cache

from .models import Order, OrderItem
from products.models import ProductVariant
from .serializer import OrderSerializer

from .permissions import IsAdminOrBot

from cart.cart import Cart
from others.decorators import auto_set_cache

from functools import wraps
from others.delete_cache import delete_cache
        

def admin_bot_check(func):
    @wraps(func)
    def wrapper(request: Request, *args, **kwargs):
        from django.conf import settings

        is_admin = request.user.is_staff
        print(request.headers)
        bot_api = request.headers.get('X-Bot-Token') == settings.BOT_API
        
        if not (is_admin or bot_api):
            return Response({'message': 'Только администраторы могут сделать это'},
                            status=status.HTTP_403_FORBIDDEN)
        return func(request, *args, **kwargs)
    return wrapper


def order_cancel_check(func):
    @wraps(func)
    def wrapper(request: Request, *args, **kwargs):
        order = kwargs.get('order')
        if order and order.status == 'отменён':
            return Response({'message': 'Заказ уже отменён!'}, status=status.HTTP_400_BAD_REQUEST)
        return func(request, *args, **kwargs)
    return wrapper


def order_exists(func):
    @wraps(func)
    def wrapper(request: Request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        if not order_id:
            return Response(
                {'message': 'Заказ не указан',},
                status=status.HTTP_400_BAD_REQUEST)
        order = get_object_or_404(Order, pk=order_id)
        kwargs['order'] = order
        return func(request, *args, **kwargs)
    return wrapper


# Create your views here.
@auto_clear_cache()
@auto_set_cache(pattern='user_')
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__telegram_id', 'status', 'phone_number']

    def create(self, request: Request):
        with transaction.atomic():
            cart = Cart(request)
            user = request.user

            if not cart:
                return Response(
                    {'error': 'Корзина пуста'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            order = Order.objects.create(
                user=user,
                phone_number=user.phone_number,
                address=user.address,
                comment=request.data.get('comment', ''),
                total_amount=0,
                status='new',
            )

            total_amount = 0

            for item in cart:
                variant_data = item['variant']

                if isinstance(variant_data, dict):
                    variant_id = variant_data.get('id')
                else:
                    variant_id = variant_data

                variant = ProductVariant.objects.select_related('product', 'color', 'size').get(id=variant_id)

                quantity = item['quantity']
                price = variant.price

                if variant.quantity < quantity:
                    transaction.set_rollback(True)
                    return Response(
                        {'error': f'Недостаточно товара: {variant.product.name}'},
                        status=400
                    )
                
                variant.quantity -= quantity
                variant.save()

                OrderItem.objects.create(
                    order=order,
                    variant=variant,
                    quantity=quantity,
                    price=price,
                    product=variant.product.name,
                    color=variant.color.color if variant.color else '',
                    size=variant.size.name if variant.size else '',
                )

                total_amount += price * quantity

            order.total_amount = total_amount
            order.save()

            cart.clear()

            delete_cache('order_list_*')
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=201)
    

@api_view(['GET'])
@order_exists
def order_get(request: Request, order_id: int, order: Order=None):
    return Response(OrderSerializer(order).data)


@api_view(['PATCH'])
@order_exists
@order_cancel_check
def cancel_order(request: Request, order_id: int, order: Order=None) -> Response:
    with transaction.atomic():
        for item in order.items.all():
            if item.variant:
                item.variant.quantity += item.quantity
                item.variant.save()

        order.status = 'cancelled'
        order.save()

        order_item = order.items.all()
        delete_cache('order_list_*')
        return Response({'message': f'Успешно отменён заказ #{order.pk}!'})


@api_view(['PATCH'])
@admin_bot_check
@order_exists
@order_cancel_check
def sent_order(request: Request, order_id: int, order: Order=None) -> Response:
    if order.status == 'shipped':
        return Response({'message': 'Заказ уже отправлен.'}, status=status.HTTP_400_BAD_REQUEST)

    order.status = 'shipped'
    order.save()

    delete_cache('order_list_*')
    return Response({'message': 'Заказ отправлен!'}, status=status.HTTP_202_ACCEPTED)


@api_view(['PATCH'])
@admin_bot_check
@order_exists
@order_cancel_check
def confirm_order(request: Request, order_id: int, order: Order=None) -> Response:
    order.status = 'delivered'
    order.save()

    delete_cache('order_list_*')
    return Response({'message': 'Заказ успешно доставлен!'}, status=status.HTTP_202_ACCEPTED)