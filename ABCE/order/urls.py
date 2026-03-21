from django.urls import path
from .views import (OrderAPIView,
                    cancel_order,
                    sent_order,
                    confirm_order, order_get)


urlpatterns = [
    path('', OrderAPIView.as_view(), name='order'),
    path('<int:order_id>/', order_get, name='order-detail'),
    path('cancel/<int:order_id>/', cancel_order, name='order-cancel'),
    path('sent/<int:order_id>/', sent_order, name='order-sent'),
    path('confirm/<int:order_id>/', confirm_order, name='order-confirm'),
]
