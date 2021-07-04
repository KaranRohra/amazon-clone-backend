from django.db import models

from products import constants


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.JSONField()
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    shipping_fee = models.PositiveIntegerField(default=0)
    category = models.CharField(
        max_length=100,
        choices=constants.CATEGORY_CHOICE,
    )

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image_url = models.ImageField(upload_to="product_images/")

    def __str__(self):
        return self.product.name
