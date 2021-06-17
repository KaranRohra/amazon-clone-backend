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
    return serializers.ProductSerializer(products, many=True).data
