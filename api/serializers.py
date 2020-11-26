from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from api.models import Order, OrderItem, Payment, Product, Store, StoreProduct
import requests
import json

# user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        return token


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password',
                  'first_name', 'last_name', 'token']

    def create(self, validated_data):
        new_user = User(**validated_data)
        new_user.set_password(validated_data['password'])
        new_user.save()
        token = RefreshToken.for_user(new_user)
        validated_data["token"] = str(token.access_token)
        return validated_data


# store

class StoreProductSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = StoreProduct
        fields = ['id', 'name', 'description', 'image', 'price']

    def get_name(self, obj):
        return obj.product.name

    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.product.image.url)

    def get_description(self, obj):
        return obj.product.description


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['uuid', 'name']


# list

class OrderItemListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['name', 'price', 'qty']

    def get_name(self, obj):
        return obj.storeproduct.product.name

    def get_price(self, obj):
        return obj.storeproduct.price


class OrderListSerializer(serializers.ModelSerializer):
    items = OrderItemListSerializer(many=True)
    store = StoreSerializer()

    class Meta:
        model = Order
        fields = ['id', 'number', 'total', 'date', 'tax', 'items', 'store']


# checkout

class OrderItemCheckoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['storeproduct', 'qty']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemCheckoutSerializer(many=True)
    store = serializers.CharField()

    class Meta:
        model = Order
        fields = ['number', 'items', 'total', 'tax', 'store']

    def create(self, validated_data):
        store = Store.objects.get(uuid=validated_data['store'])
        total = validated_data['total']
        tax = validated_data['tax']
        request = self.context.get("request")
        order_obj = Order.objects.create(
            total=total, tax=tax, user=request.user, store=store)
        order_items = validated_data['items']

        for item in order_items:
            storeproduct = item['storeproduct']
            qty = item['qty']
            subtotal = (storeproduct.price * qty)
            new_item = OrderItem(
                order=order_obj, storeproduct=storeproduct, qty=qty, subtotal=subtotal)
            new_item.save()

        return order_obj


class CheckoutLinkSerializer(serializers.Serializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['order', 'url']

    def get_url(self, obj):
        order_obj = obj
        url = "https://api.tap.company/v2/charges"

        payload = {
            "amount": f"{order_obj.total}",
            "currency": "SAR",
            "reference": {
                "transaction": "txn_0001",
                "order": f"{order_obj.number}"
            },
            "customer": {
                "first_name": f"{order_obj.user.first_name}",
                "last_name": f"{order_obj.user.last_name}",
                "email": f"{order_obj.user.email}",
                "phone": {
                    "country_code": "966",
                    "number": f"{order_obj.user.username[1:]}"
                }
            },
            "source": {
                "id": "src_all"
            },
            "post": {
                "url": "https://18eeeb80fdad.ngrok.io/api/v1/checkout/complete/"
            },
            "redirect": {
                "url": "https://18eeeb80fdad.ngrok.io/api/v1/checkout/thankyou/"
            }
        }
        payload = json.dumps(payload)
        headers = {
            'authorization': "Bearer sk_test_XKokBfNWv6FIYuTMg5sLPjhJ",
            'content-type': "application/json"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        response = response.json()
        order_obj.status = response['status']
        order_obj.save()
        return response['transaction']['url']
