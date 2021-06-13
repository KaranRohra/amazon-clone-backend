from . import serializers
from . import models


def get_products(page_number):
    number_of_products = 5 if page_number else 10

    product_end = (page_number if page_number else 1) * number_of_products
    product_start = product_end - number_of_products

    products = models.Product.objects.filter(quantity__gt=0)[product_start: product_end]
    print(product_start, product_end, models.Product.objects.all())
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
