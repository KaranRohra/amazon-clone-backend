from accounts import models as accounts_models
from cart import models as cart_models


def create_user(user_info):
    return accounts_models.User.objects.create(**user_info)


def create_cart_with_products(user_obj):
    cart = cart_models.Cart.objects.create(user=user_obj)
    products = []
    for i in range(5):
        products.append()
    cart.products.set([])

def create_empty_cart(user_obj):
    pass

def create_product():
    pass