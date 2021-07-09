from django.test import TestCase

from accounts import models as accounts_models
from cart.tests import helper as cart_helper
from orders import _private


class PlaceOrderTest(TestCase):
    def setUp(self):
        self.cart = cart_helper.Cart()
        self.user_object = self.cart.user_object
        self.user_1 = self.user_object.user_1
        self.user_4 = self.user_object.user_4
        self.user_4_address_list = self.user_object.user_4_address

    def test_place_order_without_proudcts_in_cart(self):
        with self.assertRaises(AssertionError):
            _private.place_order(self.user_4, self.user_4_address_list[0])

    def test_place_order_with_invalid_address(self):
        with self.assertRaises(accounts_models.Address.DoesNotExist):
            _private.place_order(self.user_1, -1)
