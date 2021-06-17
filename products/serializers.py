from rest_framework import serializers

from . import models


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = models.Product
        fields = [field.name for field in models.Product._meta.get_fields()]
        fields.remove("cart")


class ProductImageSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=models.Product.objects.all(), many=False)

    class Meta:
        model = models.ProductImage
        fields = "__all__"
