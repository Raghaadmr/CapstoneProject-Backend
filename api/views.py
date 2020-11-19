from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import (SignUpSerializer, MyTokenObtainPairSerializer,
                          ProductSerializer, StoreSerializer, OrderItemSerializer, OrderSerializer, StoreProductSerializer)
from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, RetrieveUpdateAPIView)
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Product, Store, Order, OrderItem, StoreProduct
from rest_framework.permissions import IsAuthenticated


class SignUp(CreateAPIView):
    serializer_class = SignUpSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ProductView(ListAPIView):
    queryset = StoreProduct.objects.all()
    serializer_class = StoreProductSerializer

    def get_queryset(self):
        store_obj = Store.objects.get(uuid=self.kwargs['store_uuid'])
        return StoreProduct.objects.filter(store=store_obj)


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class StoreListView(ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class OrderItemView(ListAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print(user)
        return user.objects.all()


class OrderView(CreateAPIView):
    serializer_class = Order
