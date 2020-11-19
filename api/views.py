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


class ProductView(RetrieveAPIView):
    queryset = StoreProduct.objects.all()
    serializer_class = StoreProductSerializer

    def get_object(self):
        return StoreProduct.objects.get(
            store__uuid=self.kwargs['store_uuid'],
            product__barcode=self.kwargs['barcode'],
        )


class StoreListView(ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


# Switch this to an order detail
class OrderItemView(ListAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print(user)
        return user.objects.all()


class OrderView(CreateAPIView):
    serializer_class = Order
