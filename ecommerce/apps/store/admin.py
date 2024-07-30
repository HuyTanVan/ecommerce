from django.contrib import admin
from .models import *
# Register your models here.
class ProductImageInline(admin.TabularInline):
    model = Image

class AttributeValueInline(admin.TabularInline):
    model = AttributeValue

class StockControlInline(admin.TabularInline):
    model = StockControl

@admin.register(Inventory)
class ProductInventoryAdmin(admin.ModelAdmin):
    readonly_fields=('sku',)
    
    inlines = [ProductImageInline, StockControlInline]

@admin.register(Attribute)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        AttributeValueInline,
    ]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("name",),
    }

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("name",),
    }