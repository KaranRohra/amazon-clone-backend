from django.test import TestCase
from django.urls import reverse

from accounts import constants
from accounts import models
from . import helper


class CrateUserAccountTest(TestCase):
    def setUp(self) -> None:
        self.url_path = reverse("accounts:create-user")
        self.data = {
            "email": constants.EMAIL,
            "password": constants.PASSWORD
        }

    def test_create_user(self):
        response = self.client.post(
            path=self.url_path,
            data=self.data
        )

        # If this doesn't raise exception then it indicates that our api is working
        models.User.objects.get(email=constants.EMAIL)
        self.assertEqual(response.json(), {"status": 201})

    def test_create_user_with_already_exist_user(self):
        helper.create_user(
            email=constants.EMAIL,
            password=constants.PASSWORD,
        )
        response = self.client.post(
            path=self.url_path,
            data=self.data
        )
        self.assertEqual(response.json(), {"status": 400})


class LoginTest(TestCase):
    def setUp(self) -> None:
        self.url_path = reverse("accounts:login-user")
        self.data = {
            "email": constants.EMAIL,
            "password": constants.PASSWORD
        }

    def test_login_with_valid_user(self):
        helper.create_user(
            email=constants.EMAIL,
            password=constants.PASSWORD,
        )
        response = self.client.post(
            path=self.url_path,
            data=self.data
        )

        self.assertEqual(response.json(), {"status": 200})

    def test_login_without_user(self):
        response = self.client.post(
            path=self.url_path,
            data=self.data
        )
        self.assertEqual(response.json(), {"status": 404})

    def test_login_with_invalid_password(self):
        helper.create_user(
            email=constants.EMAIL,
            password=constants.PASSWORD,
        )
        self.data["password"] = "wrong password"
        response = self.client.post(
            path=self.url_path,
            data=self.data,
        )
        self.assertEqual(response.json(), {"status": 404})
