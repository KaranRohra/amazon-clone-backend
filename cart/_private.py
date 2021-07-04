from cart import models
from products import models as products_models
from products import serializers as products_serializers


def get_product_from_cart(user_email):
    cart = models.Cart.objects.get(user__email=user_email)
    products = cart.products.all()
    return products_serializers.ProductSerializer(products, many=True).data


def add_product_to_cart(user_email, product_id):
    try:
        cart = models.Cart.objects.get(user__email=user_email)
        product = products_models.Product.objects.get(pk=product_id)
        cart.products.add(product)
    except products_models.Product.DoesNotExist:
        return None
    return product


def remove_product_from_cart(user_email, product_id):
    try:
        cart = models.Cart.objects.get(user__email=user_email)
        product = products_models.Product.objects.get(pk=product_id)
        cart.products.remove(product)
    except products_models.Product.DoesNotExist:
        return None
    return product
