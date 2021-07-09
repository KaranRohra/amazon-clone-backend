from django.test import TestCase

from cart import _private
from cart import models
from cart.tests import helper


class AddProductToCartTest(TestCase):
    def setUp(self) -> None:
        self.cart_object = helper.Cart()
        self.user_1 = self.cart_object.user_1
        self.user_2 = self.cart_object.user_2
        self.user_3 = self.cart_object.user_3
        self.user_1_cart = self.cart_object.user_1_cart
        self.product_1 = self.cart_object.product_2

    def test_add_product_with_valid_product(self):
        added_product = _private.add_product_to_cart(user_email=self.user_1.email, product_id=self.product_1.id)
        self.assertEqual(self.product_1, added_product)

    def test_add_product_without_product(self):
        response = _private.add_product_to_cart(
            user_email=self.user_1.email,
            product_id=-1,  # Product with id -1 is does not exist
        )
        self.assertEqual(response, None)

    def test_add_product_without_cart(self):
        with self.assertRaises(models.Cart.DoesNotExist):
            _private.add_product_to_cart(
                user_email=self.user_3.email,
                product_id=1,
            )


class RemoveProductFromCartTest(TestCase):
    def setUp(self) -> None:
        self.cart_object = helper.Cart()
        self.user_1 = self.cart_object.user_1
        self.user_2 = self.cart_object.user_2
        self.user_3 = self.cart_object.user_3
        self.user_1_cart = self.cart_object.user_1_cart
        self.product_1 = self.cart_object.product_1
        self.product_2 = self.cart_object.product_2

    def test_remove_product_with_valid_product(self):
        removed_product = _private.remove_product_from_cart(user_email=self.user_1.email, product_id=self.product_1.id)
        self.assertEqual(removed_product, self.product_1)

    def test_remove_product_without_product(self):
        response = _private.remove_product_from_cart(
            user_email=self.user_1.email,
            product_id=-1,  # Product with id -1 is does not exist
        )
        self.assertEqual(response, None)

    def test_remove_product_without_cart(self):
        with self.assertRaises(models.Cart.DoesNotExist):
            _private.remove_product_from_cart(
                user_email=self.user_3.email,
                product_id=1,
            )
