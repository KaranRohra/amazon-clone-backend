from django.conf import settings
from django.contrib.auth import models as auth_models
from django.db import models


class User(auth_models.AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    username = None
    USERNAME_FIELD = "email"
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

    """
    This help us to identify the address is deleted by user or not
    If the user delete the address we don't delete the address
    instead we set is_address_deleted to True,
    because if we delete the address it also delete the order which are related to address
    """
    is_address_deleted = models.BooleanField(
        "To delete address check this box, don't click the delete button", default=False
    )

    def __str__(self):
        return f"{self.id} __ {self.user}"
