from django.contrib import admin
from .models import Store, Product, Order, OrderItem, StoreProduct

admin.site.register(Store)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(StoreProduct)
