from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import (SignUpSerializer , MyTokenObtainPairSerializer )
from rest_framework.generics import (CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView,RetrieveUpdateAPIView)
from rest_framework_simplejwt.views import TokenObtainPairView

class SignUp(CreateAPIView):
    serializer_class = SignUpSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
