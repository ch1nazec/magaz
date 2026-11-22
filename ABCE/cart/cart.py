import logging

from rest_framework.request import Request

from decimal import Decimal
from django.conf import settings
from products.models import ProductVariant


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Cart:
    def __init__(self, request: Request) -> None:
        self.session = request.session
        self.request = request
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, variant, quantity=1, override_quantity=False):
        variant_id = str(variant.id)

        if quantity > variant.quantity:
            raise ValueError(f'Доступно только {variant.quantity} шт.')

        if variant_id not in self.cart:
            self.cart[variant_id] = {'quantity': 0,
                                     'price': str(variant.price)}
        if override_quantity:
            self.cart[variant_id]['quantity'] = quantity
        else:
            self.cart[variant_id]['quantity'] += quantity

        self.save()
    
    
    def save(self):
        self.session.modified = True
    

    def remove(self, variant):
        variant_id = str(variant.id)

        if variant_id in self.cart:
            del self.cart[variant_id]
            self.save()
    

    def __iter__(self):
        product_ids = self.cart.keys()
        variants = ProductVariant.objects.filter(id__in=product_ids).select_related('product', 'color').prefetch_related('product__images')

        cart = self.cart.copy()
        for variant in variants:
            first_image = variant.product.images.first()
            if first_image:
                image_url = self.request.build_absolute_uri(first_image.image.url)
            else:
                image_url = None

            cart[str(variant.id)]['variant'] = variant.id
            cart[str(variant.id)]['variant_data'] = {
            'id': variant.id,
            'price': str(variant.price),
            'product': {
                'id': variant.product.id,
                'name': variant.product.name,
                'slug': variant.product.slug,
            },
            'color': {
                'id': variant.color.id if variant.color else None,
                'name': variant.color.color if variant.color else None,
                'hexcode': variant.color.hexcode if variant.color else None
            } if variant.color else None,
            'size': {
                'id': variant.size.id,
                'name': variant.size.name
            },
            "image": image_url
        }
        
        for item in cart.values():
            item['price'] = str(Decimal(item['price']))
            yield item
    

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()