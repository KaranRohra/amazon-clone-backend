from rest_framework.authtoken import models as authtoken_models

from accounts import models
from accounts.tests import constants as accounts_constants


class User:
    def __init__(self):
        self.create_all_user()
        self.generate_tokens()
        self.create_address()

    def create_all_user(self):
        self.user_1 = self.create_user(accounts_constants.USER_INFO)
        self.user_2 = self.create_user(accounts_constants.USER_INFO_2)  # User 2 is without address
        self.user_3 = models.User.objects.create(email="test3@gmail.com", password="Password")  # User 3 is without cart

    def create_user(self, user_info):
        user = models.User(**user_info)
        user.set_password(user_info["password"])
        user.save()
        return user

    def delete_user(self, user):
        models.User.objects.get(email=user.email).delete()

    def generate_tokens(self):
        self.user_1_token = authtoken_models.Token.objects.create(user=self.user_1)
        self.user_2_token = authtoken_models.Token.objects.create(user=self.user_2)
        self.user_3_token = authtoken_models.Token.objects.create(user=self.user_3)

    def create_address(self):
        self.user_1_address = [  # Here we are creating three address for user_1
            models.Address.objects.create(
                user=self.user_1,
                country="Inida",
                state="Maharashtra",
                land_mark="Hira Ghat",
                pincode=421003,
                city="UNR",
                address_line="Section 18",
                phone_number_1="1234567890",
                name=accounts_constants.FIRST_NAME,
            )
            for _ in range(3)
        ]
