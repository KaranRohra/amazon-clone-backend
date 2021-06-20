from accounts import models as accounts_models
from cart import models as cart_models
from products import models as products_models


def create_user(**user_info):
    user = accounts_models.User(**user_info)
    user.set_password(user_info["password"])
    user.save()
    return user


def create_cart_with_products(user_obj, number_of_products):
    cart = cart_models.Cart.objects.create(user=user_obj)
    for _ in number_of_products:
        cart.products.set(create_product(3))


def create_product(number_of_products):
    products = []
    for _ in range(number_of_products):
        product = products_models.Product(
            name="Test product",
            description={
                "brand": "product for testing purpose",
            },
            price=1000,
            category="Mobile",
        )
        products.append(product)
    return products


def create_image(product):
    for _ in range(3):
        product.image_set.create(
            image_url="media/product_image/test_image.png"
        )
