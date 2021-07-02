from rest_framework import serializers
from rest_framework.fields import ModelField

from accounts import serializers as accounts_serializers
from products import serializers as products_serializers
from orders import models


class OrderSerializer(serializers.ModelSerializer):
    address = accounts_serializers.AddressSerializer(many=False)
    product = products_serializers.ProductSerializer(read_only=True)
    
    class Meta:
        fields = ["address", "product"]
        model = models.Order
