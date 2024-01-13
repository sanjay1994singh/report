from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=500)
    username = models.CharField(max_length=256, null=True, blank=True, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True, default=None)
    password = models.CharField(max_length=256)
    address = models.TextField(null=True, blank=True)
    dob = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True, default=None)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    phone = models.CharField(max_length=25, null=True, blank=True)
    user_type = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True)

    class Meta:
        db_table = 'user_master'

    def __str__(self):
        return str(self.username)
