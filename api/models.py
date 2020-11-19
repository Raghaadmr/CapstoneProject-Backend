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
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=7)
    barcode = models.CharField(max_length=50)
    image = models.ImageField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='stores')


    def __str__(self):
        return self.name

class Bill(models.Model):
    total = models.DecimalField(decimal_places=2, max_digits=12)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bills')
    tax = models.DecimalField(decimal_places=2, max_digits=12)
    bill_date = models.DateTimeField(auto_now_add=True)

class BillDetail(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    subtotal = models.DecimalField(decimal_places=2, max_digits=12)

# class buyer(models.Model):
#     user = models.ForeignKey(User, related_name="buyer",on_delete=models.CASCADE)
#     Firstname = models.CharField(max_length=100)
#     Lastname = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.user
#
