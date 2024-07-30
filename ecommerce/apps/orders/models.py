
from decimal import Decimal
from django.conf import settings
from django.db import models

from ecommerce.apps.store.models import Product
from ecommerce.apps.payment.models import PaymentDetail


class Order(models.Model):
    order_key = models.CharField(max_length=7, unique=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                   related_name='order_user')
    payment_key = models.OneToOneField(PaymentDetail, on_delete=models.CASCADE)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return str(self.order_key)


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    # price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.product_id)
