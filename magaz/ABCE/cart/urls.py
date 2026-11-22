from django.urls import path
from .views import CartViewAPI


urlpatterns = [
    path('', CartViewAPI.as_view(), name='cart'),
]
