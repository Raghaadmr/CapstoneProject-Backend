from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import (SignUpSerializer, MyTokenObtainPairSerializer,
                          StoreSerializer, OrderItemListSerializer, OrderItemCheckoutSerializer,
                          OrderSerializer, OrderListSerializer, StoreProductSerializer,
                          )
from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, RetrieveUpdateAPIView)
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Product, Store, Order, OrderItem, StoreProduct, Payment
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .utils import get_payment_url


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


class OrderListView(ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.orders.all()


class OrderView(CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


# Add statuses to your responses
"""
for more response status visit the link 
https://www.django-rest-framework.org/api-guide/status-codes/

"""


class CheckoutLinkView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, uuid):
        order = Order.objects.get(number=uuid)
        if order.status == "CAPTURED":
            return Response({'message': 'it\'s already paid'}, status=status.HTTP_403_FORBIDDEN)
        url = get_payment_url(order)
        return Response({'url': url}, status=status.HTTP_200_OK)


class CheckoutCompleteView(APIView):
    def post(self, request):
        # validate the data
        order_obj = Order.objects.get(number=request.data['reference']['order'])

        if (order_obj.status == "INITIATED") and (request.data['status'] == "CAPTURED"):
            Payment.objects.create(
                reference=request.data['id'],
                order=order_obj,
                tap_response_json=request.data
            )
        # order_obj.status = request.data['status']
        order_obj.save()
        return Response({"data": request.data}, status=status.HTTP_201_CREATED)


class CheckoutThankyouView(APIView):
    def get(self, request):
        return Response({'tap_id': request.GET}, status=status.HTTP_200_OK)
