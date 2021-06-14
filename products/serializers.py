from rest_framework import serializers

from . import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"


def product_with_image_serializer(products):
    """
    :param products: contains the query_set of products
    """
    if not products:  # Since NoneType object is not iterable
        return {}

    data, i = {}, 0
    for product in products:
        data[f"product_{i}"] = {
            "details": ProductSerializer(instance=product).data,
            "images": (
                "/media/" + image["image_url"]
                for image in models.ProductImage.objects.filter(product=product).values("image_url")
            )
        }
        i += 1
    return data
