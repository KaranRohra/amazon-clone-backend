from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(max_length=128)
