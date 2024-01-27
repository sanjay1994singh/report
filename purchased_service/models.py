from django.db import models

# Create your models here.
from accounts.models import CustomUser
from services.models import ServiceMaster


class ServicePurchased(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    service = models.ForeignKey(ServiceMaster, on_delete=models.PROTECT)
    price = models.IntegerField(null=True)
    discount = models.IntegerField(default=0, null=True, blank=True)
    total_price = models.IntegerField(null=True)
    qty = models.PositiveIntegerField(default=1, null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True)
    razorpay_order_id = models.CharField(max_length=100, null=True)
    razorpay_signature = models.CharField(max_length=100, null=True)
    payment_status = models.CharField(max_length=100, null=True)

    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.service.name
