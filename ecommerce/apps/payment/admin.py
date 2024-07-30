from django.contrib import admin
from .models import PaymentDetail, PaymentMethod, PaymentStatus
# Register your models here.
@admin.register(PaymentDetail)
class PaymentAdmin(admin.ModelAdmin):
    # readonly_fields=('payment_key',)
    list_display = ['pk', 'amount', 'status', 'payment_method', 'payment_key', 'customer', 'date']
    # prepopulated_fields = {'slug': ('name', )}

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['payment_type']
    # list_filter = ['in_stock', 'is_active']
    # list_editable = ['price', 'in_stock', 'stock_quantity']
    # prepopulated_fields = {'slug': ('name', )}
@admin.register(PaymentStatus)
class PaymentStatusAdmin(admin.ModelAdmin):
    list_display = ['payment_status']
    # list_filter = ['in_stock', 'is_active']
    # list_editable = ['price', 'in_stock', 'stock_quantity']
    # prepopulated_fields = {'slug': ('name', )}