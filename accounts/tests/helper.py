from accounts import models
from common.tests import constants as common_constants


class User:
    def __init__(self):
        self.user_1 = self.create_user(common_constants.USER_INFO)

    def create_user(self, user_info):
        user = models.User(**user_info)
        user.set_password(user_info["password"])
        user.save()
        return user

    def delete_user(self, user):
        models.User.objects.get(email=user.email).delete()
