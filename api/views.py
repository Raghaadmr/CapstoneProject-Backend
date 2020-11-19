from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import (SignUpSerializer , MyTokenObtainPairSerializer, ProductSerializer, StoreSerializer, BillDetailSerializer, BillSerializer )
from rest_framework.generics import (CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView,RetrieveUpdateAPIView)
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Product, Store, Bill, BillDetail
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

class BillDetailView(ListAPIView):
    serializer_class = BillDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print(user)
        return user.objects.all()


class Bill(CreateAPIView):
    serializer_class = BillSerializer
