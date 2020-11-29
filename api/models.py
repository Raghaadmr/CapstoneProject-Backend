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
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name


class StoreProduct(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='stores')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(decimal_places=2, max_digits=7)

    def __str__(self):
        return f"{self.product} in {self.store}"


class Order(models.Model):
    number = models.UUIDField(default=uuid.uuid4)
    total = models.DecimalField(decimal_places=2, max_digits=12)
    status = models.CharField(max_length=50, default="NOT PAID")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='orders')
    tax = models.DecimalField(decimal_places=2, max_digits=12)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" Order {self.id}  by {self.user} "


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    storeproduct = models.ForeignKey(StoreProduct, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    subtotal = models.DecimalField(decimal_places=2, max_digits=12)

    def __str__(self):
        return f" {self.storeproduct},  {self.order} "


class Payment(models.Model):
    reference = models.CharField(max_length=50)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment')
    date = models.DateTimeField(auto_now=True)
    # tap_response_json = models.JSONField()

    def __str__(self):
        return f"{self.order} - {self.reference}"
