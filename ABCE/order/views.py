from rest_framework import views, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Q, F

from .models import Order, OrderItem
from products.models import Product, ProductVariant
from .serializer import OrderSerializer, OrderItemSerializer

from .permissions import IsAdminOrBot

from cart.cart import Cart

from functools import wraps


def admin_check(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'message': 'Только администраторы могут сделать это'},
                            status=status.HTTP_403_FORBIDDEN)
        return func(request, *args, **kwargs)
    return wrapper


def order_cancel_check(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        order = kwargs.get('order')
        if order and order.status == 'отменён':
            return Response({'message': 'Заказ уже отменён!'}, status=status.HTTP_400_BAD_REQUEST)
        return func(request, *args, **kwargs)
    return wrapper


def order_exists(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
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
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrBot]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__telegram_id', 'status', 'phone_number']
    

    def create(self, request):
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

            serializer = OrderSerializer(order)
            return Response(serializer.data, status=201)
    

@api_view(['GET'])
@order_exists
def order_get(request, order_id, order=None):
    return Response(OrderSerializer(order).data)


@api_view(['PATCH'])
@order_exists
@order_cancel_check
def cancel_order(request, order_id, order=None):
    with transaction.atomic():
        for item in order.items.all():
            if item.variant:
                item.variant.quantity += item.quantity
                item.variant.save()

        order.status = 'cancelled'
        order.save()

        order_item = order.items.all()
        return Response({'message': f'Успешно отменён заказ #{order.pk}!'})


@api_view(['PATCH'])
@admin_check
@order_exists
@order_cancel_check
def sent_order(request, order_id, order=None):
    order.status = 'shipped'
    order.save()
    return Response({'message': 'Заказ отправлен!'}, status=status.HTTP_202_ACCEPTED)


@api_view(['PATCH'])
@admin_check
@order_exists
@order_cancel_check
def confirm_order(request, order_id, order=None):
    
    order.status = 'delivered'
    order.save()
    return Response({'message': 'Заказ успешно доставлен!'}, status=status.HTTP_202_ACCEPTED)