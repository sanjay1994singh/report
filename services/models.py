from django.db import models


# Create your models here.
class ServiceMaster(models.Model):
    name = models.CharField(max_length=256, null=True)
    desc = models.TextField(null=True)
    img = models.FileField(upload_to='service_files')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'service_master'


class ServicePrice(models.Model):
    service = models.ForeignKey(ServiceMaster, on_delete=models.CASCADE)
    month = models.IntegerField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True)

    def __str__(self):
        return str(self.service.name)

    class Meta:
        db_table = 'service_price'
