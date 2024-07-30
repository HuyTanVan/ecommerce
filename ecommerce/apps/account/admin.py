from django.contrib import admin
from .models import (Customer, Address)
# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['email', 'user_name', 'first_name', 'last_name', 'created']
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'full_name', 'phone', 'address_line', 'address_line2', 'city', 'state', 'zipcode', 'default']

