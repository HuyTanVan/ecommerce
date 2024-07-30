
from decimal import Decimal
from django.conf import settings
from django.db import models


class PaymentMethod(models.Model):
    payment_type = models.CharField(max_length=50)
    def __str__(self):
        return self.payment_type
class PaymentStatus(models.Model):
    payment_status = models.CharField(max_length=10)

    class Meta:
        # verbose_name = ('Status')
        verbose_name_plural = ('Payment status')
    def __str__(self):
        return self.payment_status
class PaymentDetail(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                   related_name='payment_customer')
    payment_method = models.ForeignKey(
        PaymentMethod, related_name="payment_method", on_delete=models.CASCADE
    )
    payment_key = models.CharField(max_length=30, editable=True, unique=True)
    status = models.ForeignKey(
        PaymentStatus, related_name="status", on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('-date',)
    def __str__(self):
        return self.payment_key
