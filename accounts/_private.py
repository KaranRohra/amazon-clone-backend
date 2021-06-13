from django.contrib import auth

from . import models
from . import serializers


def get_user(email):
    return models.User.objects.filter(email=email).first()


def create_user_account(user_info):
    user = serializers.UserSerializer(data=user_info)
    if not user.is_valid() or get_user(user.validated_data["email"]):
        return None
    user.save()
    return user


def login_user(request):
    user = auth.authenticate(
        email=request.data["email"],
        password=request.data["password"],
    )
    if user is not None:
        auth.logout(request=request)
        auth.login(request=request, user=user)
        return user
    return None
