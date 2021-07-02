from cart import models


def remove_products_from_cart(user):
    cart = models.Cart.objects.get(user=user)
    cart.products.clear()


def get_all_products_from_cart(user):
    return models.Cart.objects.get(user=user).products.all()
