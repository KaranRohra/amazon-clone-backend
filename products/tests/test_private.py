from django.test import TestCase

# from common.tests import helper
# from products import _private


class GetProductsTest(TestCase):
    def setUp(self) -> None:
        self.page_number = 1
        self.last_page_number = 2
        self.invalid_page_number = -1

    def test_get_product_with_products(self):
        # products = helper.create_products(number_of_products=10)
        # expected_response = products[:5]

        # response = _private.get_products()
        # TODO
        pass
