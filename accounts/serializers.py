from rest_framework import fields, serializers

from accounts import models
from cart import models as cart_models


class UserSerializer(serializers.ModelSerializer):
    def create(self, validate_data):
        user = models.User(
            **validate_data
        )
        user.set_password(validate_data["password"])
        user.save()
        cart_models.Cart.objects.create(user=user)
        return user
    
    class Meta:
        model = models.User
        # fields = "__all__"
        exclude = ["groups", "user_permissions", "password"]


class AddressSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return models.Address.objects.create(**validated_data)
    class Meta:
        model = models.Address
        fields = "__all__"
