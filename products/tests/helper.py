from products import models


class Product:
    def __init__(self):
        self.create_products()
        self.create_images()

    def create_products(self):
        self.product_1 = models.Product.objects.create(
            name="Test product",
            description={
                "brand": "product for testing purpose",
            },
            price=1000,
            category="Mobile",
        )
        self.product_2 = models.Product.objects.create(
            name="Test product",
            description={
                "brand": "product for testing purpose",
            },
            price=1000,
            category="Mobile",
        )

    def create_images(self):
        self.product_1_image = models.ProductImage.objects.create(
            product=self.product_1, image_url="media/product_image/test_image.png"
        )
        self.product_2_image = models.ProductImage.objects.create(
            product=self.product_2, image_url="media/product_image/test_image.png"
        )
