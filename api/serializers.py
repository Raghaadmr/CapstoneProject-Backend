from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from api.models import Product, Bill, BillDetail, Store


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
        fields = [ 'username', 'email', 'password',
                  'first_name', 'last_name', 'token']

    def create(self, validated_data):
        new_user = User(**validated_data)
        new_user.set_password(validated_data['password'])
        new_user.save()
        token = RefreshToken.for_user(new_user)
        validated_data["token"] = str(token.access_token)
        return validated_data


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image','description']

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name','uuid']

class BillDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillDetail
        fields = ['id', 'bill', 'subtotal' 'product', 'qty']

class BillSerializer(serializers.ModelSerializer):
    details = BillDetailSerializer(many=True)
    class Meta:
        model = Bill
        fields = ['total', 'tax', 'bill_date', 'details']
    def create(self, validated_data):
        total = validated_data['total']
        tax = validated_data['tax']
        request = self.context.get("request")
        checkout = Bill(total=total, tax=tax, user=request.user)
        checkout.save()
        details = validated_data['details']
        for detail in details:
            product = item['product']
            qty = item['qty']
            if product < 6 :
                bill_detail = BillDetail(checkout=checkout, qty=qty, product=product)
                bill_detail.save()
            else:
                bill_detail.delete()
                raise serializers.ValidationError("ONLY 5 PRODUCTS ARE ALLOWED")
        return validated_data
