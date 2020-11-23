from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from api.models import Product, Order, OrderItem, Store, StoreProduct


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


class StoreProductSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = StoreProduct
        fields = ['id','name', 'description', 'image', 'price']

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
        fields = ['name', 'uuid']

#Order list
class OrderItemSerializer(serializers.ModelSerializer):
    # name = serializers.SerializerMethodField()
    # price = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = ['storeproduct','qty']

    # def get_name(self, obj):
    #     return obj.storeproduct.product.name

    # def get_price(self, obj):
    #     return obj.items.storeproduct.price



class OrderListSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id','number', 'total', 'date', 'tax', 'items']

#checkout
# class OrderItemSerializer(serializers.ModelSerializer):
#     product = serializers.SerializerMethodField()
#     class Meta:
#         model = OrderItem
#         fields = ['id', 'product', 'qty']
#     def get_product(self, obj):
#         return obj.storeproduct.product

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'total', 'tax', 'items']

    def create(self, validated_data):
        total = validated_data['total']
        tax = validated_data['tax']
        request = self.context.get("request")
        order_obj = Order.objects.create(
            total=total, tax=tax, user=request.user)
        order_items = validated_data['items']

        for item in order_items:
            storeproduct = item['storeproduct']
            qty = item['qty']
            # storeproduct_obj = StoreProduct.objects.get(id=storeproduct)
            subtotal = (storeproduct.price * qty)
            new_item = OrderItem(order=order_obj, qty=qty, storeproduct=storeproduct, subtotal=subtotal)
            new_item.save()

        return validated_data
