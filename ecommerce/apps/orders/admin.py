from django.contrib import admin
from ecommerce.apps.orders.models import (Order, OrderItem)
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk','order_key', 'total_paid', 'user_id', 'payment_key','created', 'updated']
    # prepopulated_fields = {'slug': ('name', )}

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['pk','order_id', 'product_id', 'quantity']
    # list_filter = ['in_stock', 'is_active']
    # list_editable = ['price', 'in_stock', 'stock_quantity']
    # prepopulated_fields = {'slug': ('name', )}