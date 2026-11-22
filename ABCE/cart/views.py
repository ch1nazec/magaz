from rest_framework.response import Response
from rest_framework.request import Request

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import views
from .cart import Cart
from products.models import ProductVariant


# Create your views here.
class CartViewAPI(views.APIView):
    def post(self, request: Request):
        with transaction.atomic():
            cart = Cart(request)

            productvariant_id = request.data.get('id')
            quantity = request.data.get('quantity')

            productvariant = get_object_or_404(ProductVariant, pk=productvariant_id)
            cart.add(productvariant, quantity)
            return Response({
                'message': 'Добавлено в корзину',
                "cart": {
                    'id': productvariant_id,
                    'items': list(cart),
                    'total_price': str(cart.get_total_price()),
                    'quantity': len(cart)
                    }})
    
    def get(self, request: Request):
        cart = Cart(request)

        return Response({
            'items': list(cart),
            'total_price': str(cart.get_total_price()),
            'total_items': len(cart)})
    
    def delete(self, request: Request):
        with transaction.atomic():
            cart = Cart(request)
            cart.clear()

            return Response({'message': 'Успешно'})