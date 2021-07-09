from accounts.tests import helper as accounts_helper
from cart import models
from products.tests import helper as products_helper


class Cart:
    def __init__(self):
        self.user_object = accounts_helper.User()
        self.product_object = products_helper.Product()
        self.user_1 = self.user_object.user_1
        self.user_2 = self.user_object.user_2
        self.user_3 = self.user_object.user_3
        self.user_4 = self.user_object.user_4
        self.product_1 = self.product_object.product_1
        self.product_2 = self.product_object.product_2
        self.user_1_cart_products = [
            self.product_1,
            self.product_2,
        ]

        self.create_cart()
        self.add_products_to_cart()

    def create_cart(self):
        self.user_1_cart = models.Cart.objects.create(user=self.user_1)
        self.user_2_cart = models.Cart.objects.create(user=self.user_2)
        self.user_4_cart = models.Cart.objects.create(user=self.user_4)

    def add_products_to_cart(self):
        self.user_1_cart.products.set(self.user_1_cart_products)
