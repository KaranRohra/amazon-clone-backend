from django.test import TestCase

from accounts import _private
from accounts import constants
from . import helper


class GetUserTest(TestCase):
    def test_get_user_with_known_email(self):
        expected_user = helper.create_user(
            email=constants.EMAIL,
            password=constants.PASSWORD
        )
        user = _private.get_user(
            email=constants.EMAIL
        )
        self.assertEqual(user, expected_user)

    def test_get_user_with_unknown_email(self):
        user = _private.get_user(
            email=constants.UNKNOWN_EMAIL
        )
        self.assertEqual(user, None)


class CreateUserTest(TestCase):
    def test_create_user_account_already_exist(self):
        helper.create_user(
            email=constants.EMAIL,
            password=constants.PASSWORD
        )

        user = _private.create_user_account({
            "email": constants.EMAIL,
            "password": constants.PASSWORD,
        })
        self.assertEqual(user, None)
