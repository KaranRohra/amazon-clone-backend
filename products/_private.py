from django.db import models as db_models

from products import models


def get_products(page_number, search_by):
    """
    :param page_number: contains page_number
    return the 5 product according to page_number

    :return <= 5 products
    """
    if page_number <= 0:
        raise ValueError("Invalid page number")
    
    end_product_index = page_number * 5
    start_product_index = end_product_index - 5

    res = models.Product.objects.filter(
        db_models.Q(name__icontains=search_by) |
        db_models.Q(category__icontains=search_by),
        quantity__gt=0
    )
    if res:
        return res[start_product_index:end_product_index]
    return models.Product.objects.all()[start_product_index:end_product_index]
