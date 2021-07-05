from accounts import models as accounts_models
from cart import models as cart_models
from products import models as products_models


def create_cart(user_obj, number_of_products):
    cart = cart_models.Cart.objects.create(user=user_obj)
    cart.products.set(create_products(number_of_products))
    return cart


def create_products(number_of_products):
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
        product.save()
        products.append(product)
        create_images(product)
    return products


def create_images(product):
    for _ in range(3):
        products_models.ProductImage(product=product, image_url="media/product_image/test_image.png").save()


def create_address(user, number_of_address=1):
    return [
        accounts_models.Address.objects.create(
            user=user,
            country="Inida",
            state="Maharashtra",
            land_mark="Hira Ghat",
            pincode=421003,
            city="UNR",
            address_line="Section 18",
            phone_number_1="1234567890",
        )
        for _ in range(number_of_address)
    ]
