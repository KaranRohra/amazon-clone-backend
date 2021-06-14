from . import serializers
from . import models


def get_products(page_number):
    """
    :param page_number: contains page_number
    if page_number is 0 we send 5 records of product
    else 10 records of product
    """
    number_of_products = 5 if page_number else 10

    product_end = (page_number if page_number else 1) * number_of_products
    product_start = product_end - number_of_products

    products = models.Product.objects.filter(quantity__gt=0)[product_start: product_end]
    data = {}
    for i, product in zip(range(0, number_of_products), products):
        data[f"product_{i}"] = {
            "details": serializers.ProductSerializer(instance=product).data,
            "images": (
                "/media/" + image["image_url"]
                for image in models.ProductImage.objects.filter(product=product).values("image_url")
            )
        }
    return data
