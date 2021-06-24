from django.test import TestCase
from django.urls import reverse

from common.tests import helper
from common.tests import constants


class ProductFromCartTest(TestCase):
    def setUp(self):
        self.api_url = "cart:get-products"
        self.user_info = {
            "email": constants.EMAIL,
            "password": constants.PASSWORD
        }

    def test_get_product_from_cart_from_unauthenticated_user(self):
        response = self.client.get(
            path=reverse(self.api_url)
        )
        expected_response = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(expected_response, response.json())
