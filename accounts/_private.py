from . import models
from . import serializers


def get_user(email, password=None):
    user = models.User.objects.filter(email=email).first()
    if user:
        if (password and user.check_password(password)) or not password:
            return user
    return None 


def create_user_account(user_info):
    user = serializers.UserSerializer(data=user_info)
    if user.is_valid():
        if get_user(user.validated_data["email"]):
            return None
        user.save()
        return user
    return None

