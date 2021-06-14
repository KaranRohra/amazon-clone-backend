import re

from django.contrib import auth

from . import models
from . import serializers


def get_user(email):
    """
    :param email: contains user email
    :return user if user exist with email else None
    """
    return models.User.objects.filter(email=email).first()


def create_user_account(user_info):
    """
    :param user_info: contains user_info in dict
    :return user if user is not exist and valid info else None

    Example:
    user_info = {
        "email": "user@gmail.com",
        "password": "password"
    }
    """
    user = serializers.UserSerializer(data=user_info)
    if not user.is_valid() or get_user(user.validated_data["email"]):
        return None
    user.save()
    return user


def login_user(request):
    """
    :param request: HttpRequest object helps to get data from request.data variable of type dict
    :return user if user exist and valid info else None
    """
    user = auth.authenticate(
        email=request.data["email"],
        password=request.data["password"],
    )
    if user is not None:
        auth.logout(request=request)
        auth.login(request=request, user=user)
        return user
    return None


def is_email_valid(email):
    """
    :param email: user email
    :return True if email is valid else False

    email_regex contains email regex refer https://regexr.com/3e48o
    which helps to identify the email is valid or not
    Example:
    Valid:
        admin@admin.com
    Invalid:
        admin.com
    """
    email_regex = re.compile(r"^[\w-]+@([\w-]+\.)+[\w-]{2,4}$")
    return True if re.search(email_regex, email) else False
