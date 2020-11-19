from django.contrib import admin
from .models import Store, Product, Bill, BillDetail
# Register your models here.
admin.site.register(Store)
admin.site.register(Product)
admin.site.register(Bill)
admin.site.register(BillDetail)
