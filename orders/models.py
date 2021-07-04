from django.db import models

from accounts import models as accounts_models
from products import models as products_models


class Order(models.Model):
    user = models.ForeignKey(accounts_models.User, on_delete=models.CASCADE)
    address = models.ForeignKey(accounts_models.Address, on_delete=models.CASCADE)
    product = models.ForeignKey(products_models.Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
