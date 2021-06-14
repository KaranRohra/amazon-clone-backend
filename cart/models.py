from django.db import models

from accounts import models as accounts_models
from products import models as product_models


class Cart(models.Model):
    user = models.OneToOneField(
        to=accounts_models.User,
        on_delete=models.CASCADE,
    )
    products = models.ManyToManyField(
        to=product_models.Product,
        default=None,
    )

    def __str__(self):
        return self.user.email
