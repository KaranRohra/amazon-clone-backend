from accounts import public as accounts_public
from cart import public as cart_public
from orders import models


def place_order(user, address):
    """
    :param user: place the order of specify user
    :param address: place the order on this address
    :return True if order_placed else False
    """
    products = cart_public.get_all_products_from_cart(user=user)
    assert products, "No products available to place order"
    address = accounts_public.get_address_by_pk(pk=address)
    for product in products:
        models.Order.objects.create(
            user=user,
            address=address,
            product=product,
        )
    cart_public.remove_products_from_cart(user=user)
