from rest_framework import serializers

from . import models


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(max_length=128)

    def create(self, validate_data):
        user = models.User(
            **validate_data
        )
        user.set_password(validate_data["password"])
        user.save()
        return user
