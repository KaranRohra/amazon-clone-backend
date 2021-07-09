from django.db import models as db_models

from products import models


def get_products(page_number, search_by=""):
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
        db_models.Q(name__icontains=search_by) | db_models.Q(category__icontains=search_by),
    )
    if res:
        return res[start_product_index:end_product_index]
    return models.Product.objects.all()[start_product_index:end_product_index]


def get_products_count_based_on_search_value(search_value):
    """
    :param search_value: contains search value which help to filter products
    :return count of products which are satisfied search value
    else all products count which are present in database
    """
    number_of_products = models.Product.objects.filter(
        db_models.Q(name__icontains=search_value) | db_models.Q(category__icontains=search_value),
    ).count()
    if not number_of_products:
        number_of_products = models.Product.objects.count()
    return {"number_of_products": number_of_products}
