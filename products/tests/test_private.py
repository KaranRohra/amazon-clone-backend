from django.test import TestCase
# from django.urls import reverse
#
# from backend.products import _private as products_private


# def create_product(data):
#     return products_models.Product.objects.create(**data)
#
#
# class GetProductTest(TestCase):
#     def test_get_product_without_products(self):
#         response = products_private.get_products(
#             page_number=0
#         )
#         self.assertEqual({}, response.json())
#
#     def test_get_product_with_page_number_as_0(self):
#         expected_data = []
#         for i in range(10):
#             expected_data.append(create_product(data={
#                 "name": "iphone",
#                 "description": {
#                     "brand": "apple",
#                     "color": "blue",
#                 },
#                 "price": 100,
#                 "shipping_fee": 0,
#                 "quantity": 1,
#             }))
#
#         self.assertEqual()
