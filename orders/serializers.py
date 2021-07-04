from rest_framework import serializers

from accounts import serializers as accounts_serializers
from orders import models
from products import serializers as products_serializers


class OrderSerializer(serializers.ModelSerializer):
    address = accounts_serializers.AddressSerializer(many=False)
    product = products_serializers.ProductSerializer(read_only=True)

    class Meta:
        fields = "__all__"
        model = models.Order
