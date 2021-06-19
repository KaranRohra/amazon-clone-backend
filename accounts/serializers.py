from rest_framework import serializers

from accounts import models


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(max_length=128, write_only=True)
    is_staff = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(default=False)

    def create(self, validate_data):
        user = models.User(
            **validate_data
        )
        user.set_password(validate_data["password"])
        user.save()
        return user
