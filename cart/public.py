from cart import models


def remove_products_from_cart(user):
    cart = models.Cart.objects.get(user=user)
    cart.products.clear()


def get_all_products_from_cart(user):
    try:
        products = models.Cart.objects.get(user=user).products.all()
    except models.Cart.DoesNotExist:
        raise models.Cart.DoesNotExist("User not registered")
    return products
