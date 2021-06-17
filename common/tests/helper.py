from accounts import models as accounts_models
from cart import models as cart_models


def create_user(**user_info):
    user = accounts_models.User(**user_info)
    user.set_password(user_info["password"])
    user.save()
    return user


def create_cart_with_products(user_obj):
    cart = cart_models.Cart.objects.create(user=user_obj)
    # products = []
    # for i in range(5):
    #     products.append()
    # cart.products.set([])


def create_empty_cart(user_obj):
    pass


def create_product():
    pass
