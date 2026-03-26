from django.urls import path, include
from .views import (OrderViewSet,
                    cancel_order,
                    sent_order,
                    confirm_order, order_get)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', OrderViewSet, basename='orders')


urlpatterns = [
    path('', include(router.urls)),
    path('<int:order_id>/', order_get, name='order-detail'),
    path('cancel/<int:order_id>/', cancel_order, name='order-cancel'),
    path('sent/<int:order_id>/', sent_order, name='order-sent'),
    path('confirm/<int:order_id>/', confirm_order, name='order-confirm'),
]
