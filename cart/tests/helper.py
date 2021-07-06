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
        self.product_1 = self.product_object.product_1
        self.product_2 = self.product_object.product_2

        self.create_cart()

    def create_cart(self):
        self.user_1_cart = models.Cart.objects.create(user=self.user_1)
        self.user_2_cart = models.Cart.objects.create(user=self.user_2)

    def add_products_to_cart(self):
        self.user_1_cart.products.add(self.product_1)
