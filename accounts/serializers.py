import os

from rest_framework import serializers

from accounts import models
from cart import models as cart_models


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validate_data):
        validate_data["is_active"] = True

        # This help us to create superuser with the help of virtual env in local or in heroku "env variables"
        validate_data["is_superuser"] = bool(os.environ.get("need_superuser"))
        validate_data["is_staff"] = bool(os.environ.get("need_superuser"))

        user = models.User(**validate_data)
        user.set_password(validate_data["password"])
        user.save()
        cart_models.Cart.objects.create(user=user)
        return user

    class Meta:
        model = models.User
        exclude = ["groups", "user_permissions", "is_staff", "is_superuser"]


class AddressSerializer(serializers.ModelSerializer):
    is_address_deleted = serializers.BooleanField(default=False, write_only=True)

    class Meta:
        model = models.Address
        read_only_fields = ("user",)
        fields = "__all__"
