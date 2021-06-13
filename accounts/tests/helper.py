from accounts import models


def create_user(email, password=None):
    user = models.User(
        email=email
    )
    if password:
        user.set_password(password)
    user.save()
    return user
