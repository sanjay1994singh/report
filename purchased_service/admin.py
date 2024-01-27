from django.contrib import admin
from .models import ServicePurchased


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service', 'total_price', 'month', 'payment_status')


admin.site.register(ServicePurchased, ServiceAdmin)
