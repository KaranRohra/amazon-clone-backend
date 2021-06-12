from django.test import TestCase

from accounts import models
from accounts import _private
from accounts import constants


def create_user(email, password=None):
    user = models.User(
        email=email
    )
    if password:
        user.set_password(password)
    user.save()
    return user


class UserActions(TestCase):
    def test_get_user_with_known_email(self):
        expected_user = create_user(constants.EMAIL)
        user = _private.get_user(
            email=constants.EMAIL
        )
        self.assertEqual(user, expected_user)

    def test_get_user_with_unknown_email(self):
        user = _private.get_user(
            email=constants.UNKNOWN_EMAIL
        )
        self.assertEqual(user, None)

    def test_get_user_with_email_and_password(self):
        expected_user = create_user(
            email=constants.EMAIL,
            password=constants.PASSWORD,
        )
        user = _private.get_user(
            email=constants.EMAIL,
            password=constants.PASSWORD,
        )
        self.assertEqual(user, expected_user)

    def test_get_user_with_invalid_password(self):
        create_user(
            email=constants.EMAIL,
            password=constants.PASSWORD,
        )
        user = _private.get_user(
            email=constants.EMAIL,
            password="invalid password",
        )
        self.assertEqual(user, None)

    def test_create_user_account_already_exist(self):
        create_user(
            email=constants.EMAIL,
            password=constants.PASSWORD
        )

        user = _private.create_user_account({
            "email": constants.EMAIL,
            "password": constants.PASSWORD,
        })
        self.assertEqual(user, None)
