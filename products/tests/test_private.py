from django.test import TestCase

from products import _private
from products.tests import helper


class GetProductByPageNumberTest(TestCase):
    def setUp(self):
        self.product = helper.Product()
        self.product_list = self.product.product_list
        self.search_value_mobile = "mobile"
        self.search_invalid_value = "invalid value"

    def test_get_product_with_valid_page_number_as_1(self):
        products = _private.get_products(page_number=1)
        expected_product = self.product_list[:5]
        self.assertEqual(expected_product, products)

    def test_get_product_with_page_number_as_2(self):
        products = _private.get_products(page_number=2)

        # Make sure after adding more products, update 6 to number of products
        expected_product = self.product_list[5:6]
        self.assertEqual(expected_product, products)

    def test_get_product_with_page_number_and_search_value(self):
        products = _private.get_products(page_number=1, search_by=self.search_value_mobile)
        expected_products = self.product_list[: self.product.mobile_product_count]
        self.assertEqual(expected_products, products)

    def test_get_product_with_page_number_out_of_products_count(self):
        products = _private.get_products(
            page_number=100,
        )
        expected_products = []
        self.assertEqual(expected_products, products)

    def test_get_product_with_invalid_search_value(self):
        products = _private.get_products(page_number=1, search_by=self.search_invalid_value)
        expected_products = self.product_list[:5]
        self.assertQuerysetEqual(expected_products, products)

    def test_get_product_with_invalid_page_number(self):
        with self.assertRaises(ValueError):
            _private.get_products(page_number=-1)


class GetProductCountTest(TestCase):
    def setUp(self):
        self.product = helper.Product()
        self.product_list = self.product.product_list
        self.search_value_mobile = "mobile"
        self.search_invalid_value = "invalid value"
        self.product_name_startswith_test = "Test"

    def test_get_product_count_with_valid_search_value(self):
        product_count = _private.get_products_count_based_on_search_value(search_value=self.search_value_mobile)
        expected_product_count = {
            "number_of_products": self.product.mobile_product_count,
        }
        self.assertEqual(expected_product_count, product_count)

    def test_get_product_count_with_invalid_search_value(self):
        product_count = _private.get_products_count_based_on_search_value(search_value=self.search_invalid_value)
        expected_product_count = {"number_of_products": len(self.product_list)}
        self.assertEqual(expected_product_count, product_count)

    def test_get_product_count_search_with_product_name(self):
        product_count = _private.get_products_count_based_on_search_value(
            search_value=self.product_name_startswith_test
        )
        expected_product_count = {"number_of_products": len(self.product_list)}
        self.assertEqual(expected_product_count, product_count)

    def test_get_product_count_without_products(self):
        self.product.delete_all_products()
        product_count = _private.get_products_count_based_on_search_value(
            search_value=self.product_name_startswith_test
        )
        expected_product_count = {
            "number_of_products": 0,  # Since there are not products
        }
        self.assertEqual(expected_product_count, product_count)
