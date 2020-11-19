from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import (
    SignUpSerializer , MyTokenObtainPairSerializer, 
    ProductSerializer, StoreSerializer, 
    OrderItemSerializer, OrderSerializer
)
from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView,RetrieveUpdateAPIView
)
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Product, Store, Order, OrderItem
from rest_framework.permissions import IsAuthenticated


class SignUp(CreateAPIView):
    serializer_class = SignUpSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ProductView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class StoreList(ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer



# [
#     {
#         "store_product": 1,
#         "qty": 3,
#     },
#     {
#         "product": 1,
#         "qty": 3,
#     },
# ]

class Order(CreateAPIView):
    serializer_class = OrderSerializer
