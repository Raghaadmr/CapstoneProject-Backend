from django.contrib import admin
from .models import Store, Product, Order, OrderItem, StoreProduct, Payment


class StoreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


admin.site.register(Store, StoreAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'barcode']
    search_fields = ['name', 'barcode']


admin.site.register(Product, ProductAdmin)


class StoreProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'store', 'price']
    search_fields = ['store__name', 'product__name', 'product__barcode']
    list_filter = ['store']
    list_editable = ['price']


admin.site.register(StoreProduct, StoreProductAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['number', 'user', 'store', 'total']
    search_fields = ['number', 'user']
    list_filter = ['date', 'store']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Payment)
