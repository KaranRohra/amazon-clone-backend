from django.test import TestCase

from accounts.tests import helper as accounts_helper
from cart import _private
from cart import models
from common.tests import constants as common_constants
from common.tests import helper
from products import serializers


class GetProductTest(TestCase):
    def setUp(self) -> None:
        self.user_obj = accounts_helper.User()
        self.user = self.user_obj.user_1

    def test_get_products_with_valid_products(self):
        cart = helper.create_cart(user_obj=self.user, number_of_products=3)
        expected_response = serializers.ProductSerializer(cart.products.all(), many=True).data
        response = _private.get_product_from_cart(user_email=self.user.email)
        self.assertEqual(expected_response, response)

    def test_get_products_without_cart(self):
        with self.assertRaises(models.Cart.DoesNotExist):
            _private.get_product_from_cart(user_email=self.user.email)

    def test_get_products_without_user(self):
        with self.assertRaises(models.Cart.DoesNotExist):
            _private.get_product_from_cart(user_email=common_constants.UNKNOWN_EMAIL)

    def test_get_products_without_products(self):
        cart = helper.create_cart(user_obj=self.user, number_of_products=0)
        expected_response = serializers.ProductSerializer(cart.products.all(), many=True).data
        response = _private.get_product_from_cart(user_email=self.user.email)
        self.assertEqual(expected_response, response)


class AddProductToCartTest(TestCase):
    def setUp(self) -> None:
        self.user_object = accounts_helper.User()
        self.user = self.user_object.user_1

    def test_add_product_with_valid_product(self):
        cart = helper.create_cart(
            user_obj=self.user,
            number_of_products=0,  # 0 Indicating empty cart
        )
        products = helper.create_products(number_of_products=1)
        added_product = _private.add_product_to_cart(user_email=self.user.email, product_id=products[0].id)
        self.assertEqual(cart.products.get(id=products[0].id), added_product)
        self.assertEqual(added_product, products[0])

    def test_add_product_without_product(self):
        helper.create_cart(
            user_obj=self.user,
            number_of_products=0,  # 0 Indicating empty cart
        )
        response = _private.add_product_to_cart(
            user_email=self.user.email,
            product_id=1,  # Product with id 1 is does not exist
        )
        self.assertEqual(response, None)

    def test_add_product_without_cart(self):
        with self.assertRaises(models.Cart.DoesNotExist):
            _private.add_product_to_cart(
                user_email=self.user.email,
                product_id=1,
            )


class RemoveProductFromCartTest(TestCase):
    def setUp(self) -> None:
        self.user_object = accounts_helper.User()
        self.user = self.user_object.user_1

    def test_remove_product_with_valid_product(self):
        cart = helper.create_cart(
            user_obj=self.user,
            number_of_products=1,
        )
        self.assertEqual(cart.products.count(), 1)  # Before remove

        product = cart.products.get(id=1)
        removed_product = _private.remove_product_from_cart(user_email=self.user.email, product_id=1)
        self.assertEqual(cart.products.count(), 0)  # After remove
        self.assertEqual(removed_product, product)

    def test_remove_product_without_product(self):
        helper.create_cart(
            user_obj=self.user,
            number_of_products=0,  # 0 Indicating empty cart
        )
        response = _private.remove_product_from_cart(
            user_email=self.user.email,
            product_id=1,  # Product with id 1 is does not exist
        )
        self.assertEqual(response, None)

    def test_remove_product_without_cart(self):
        with self.assertRaises(models.Cart.DoesNotExist):
            _private.remove_product_from_cart(
                user_email=self.user.email,
                product_id=1,
            )
