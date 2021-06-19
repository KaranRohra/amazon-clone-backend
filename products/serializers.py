from rest_framework import serializers

from products import models


class ProductImageSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=models.Product.objects.all(), many=False)

    class Meta:
        model = models.ProductImage
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(read_only=True, many=True)

    class Meta:
        model = models.Product
        fields = [field.name for field in models.Product._meta.get_fields()]
        fields.remove("cart")
