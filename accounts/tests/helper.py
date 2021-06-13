from accounts import models


def create_user(email, password):
    user = models.User(
        email=email
    )
    user.set_password(password)
    user.save()
    return user
