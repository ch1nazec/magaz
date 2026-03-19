from rest_framework import viewsets
from .models import Order, OrderItem
from .serializer import OrderSerializer, OrderItemSerializer


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem