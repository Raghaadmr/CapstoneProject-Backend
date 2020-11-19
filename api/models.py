from django.db import models
from django.utils.timezone import timedelta, timezone
from django.contrib.auth.models import User
import uuid


class Store(models.Model):
    name = models.CharField(max_length=191)
    uuid = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=191)
    description = models.TextField(null=True, blank=True)
    barcode = models.CharField(max_length=50)
    image = models.ImageField()

    def __str__(self):
        return self.name


class StoreProduct(models.Model):
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name='stores')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(decimal_places=2, max_digits=7)


class Order(models.Model):
    number = models.UUIDField(default=uuid.uuid4)
    total = models.DecimalField(decimal_places=2, max_digits=12)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders')
    tax = models.DecimalField(decimal_places=2, max_digits=12)
    date = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    store_product = models.ForeignKey(StoreProduct, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    subtotal = models.DecimalField(decimal_places=2, max_digits=12)
