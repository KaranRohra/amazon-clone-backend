from django.db import models
from django.contrib.auth import models as auth_models
from django.conf import settings


class User(auth_models.AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    land_mark = models.CharField(max_length=50)
    address_line = models.TextField()
    pincode = models.IntegerField()
    name = models.CharField(max_length=50, default="Anonymus")
    phone_number_1 = models.CharField("Phone number 1", max_length=20, default="Not available")
    phone_number_2 = models.CharField("Phone number 2 (Optional)", max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.user} __ {self.country} __ {self.state}"
