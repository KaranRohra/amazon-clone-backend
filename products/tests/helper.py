from products import models


class Product:
    def __init__(self):
        self.create_products()
        self.create_images()

    def create_products(self):
        self.product_info_1 = {
            "name": "Test product",
            "description": {
                "brand": "product for testing purpose",
            },
            "price": 1000,
            "category": "Mobile",
        }
        self.product_info_2 = {
            **self.product_info_1,
            "name": "Test 2 Product",
            "category": "TV",
        }
        self.product_1 = models.Product.objects.create(**self.product_info_1)
        self.product_2 = models.Product.objects.create(**self.product_info_1)
        self.product_3 = models.Product.objects.create(**self.product_info_1)
        self.product_4 = models.Product.objects.create(**self.product_info_1)
        self.product_5 = models.Product.objects.create(**self.product_info_2)
        self.product_6 = models.Product.objects.create(**self.product_info_2)
        self.product_list = [
            self.product_1,
            self.product_2,
            self.product_3,
            self.product_4,
            self.product_5,
            self.product_6,
        ]

        self.mobile_product_count = 4
        self.tv_product_count = 2

    def create_images(self):
        self.product_image = {"product": self.product_2, "image_url": "media/product_image/test_image.png"}
        self.product_1_image = models.ProductImage.objects.create(**self.product_image)
        self.product_2_image = models.ProductImage.objects.create(**self.product_image)

    def delete_all_products(self):
        for product in self.product_list:
            product.delete()
