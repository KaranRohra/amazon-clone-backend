import os

from rest_framework import serializers

from accounts import models
from cart import models as cart_models


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    def create(self, validate_data):
        validate_data["is_active"] = True

        # This help us to create superuser from heroku server
        validate_data["is_superuser"] = True if os.environ.get("need_superuser") else False
        validate_data["is_staff"] = True if os.environ.get("need_superuser") else False

        user = models.User(
            **validate_data
        )
        user.set_password(validate_data["password"])
        user.save()
        cart_models.Cart.objects.create(user=user)
        return user
    
    class Meta:
        model = models.User
        exclude = ["groups", "user_permissions", "is_staff", "is_superuser"]


class AddressSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return models.Address.objects.create(**validated_data)
    
    class Meta:
        model = models.Address
        fields =  "__all__"
