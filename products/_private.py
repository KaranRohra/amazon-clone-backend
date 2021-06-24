from products import models


def get_products(page_number):
    """
    :param page_number: contains page_number
    return the 5 product according to page_number

    :return <= 5 products
    """
    end_product_index = page_number * 5
    start_product_index = end_product_index - 5

    return models.Product.objects.filter(quantity__gt=0)[
        start_product_index:end_product_index
    ]
