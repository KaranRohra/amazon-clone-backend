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
        expected_response = {
            "status": 201,
            "status_text": "Account created successfully"
        }
        self.assertEqual(response.json(), expected_response)

    def test_create_user_with_already_exist_user(self):
        helper.create_user(
            email=constants.EMAIL,
            password=constants.PASSWORD,
        )
        response = self.client.post(
            path=self.url_path,
            data=self.data
        )
        expected_response = {
            "status": 400,
            "status_text": "Account already exist"
        }
        self.assertEqual(response.json(), expected_response)

    def test_create_user_with_invalid_email(self):
        self.data["email"] = constants.INVALID_EMAIL_SYNTAX
        response = self.client.post(
            path=self.url_path,
            data=self.data,
        )
        expected_response = {
            "status": 406,
            "status_text": "Invalid email"
        }
        self.assertEqual(response.json(), expected_response)


class LoginTest(TestCase):
    def setUp(self) -> None:
        self.url_path = reverse("accounts:login")
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
        expected_response = {
            "status": 200,
            "status_text": "Login successfully"
        }
        self.assertEqual(self.client.login(**self.data), True)
        self.assertEqual(response.json(), expected_response)

    def test_login_without_user(self):
        response = self.client.post(
            path=self.url_path,
            data=self.data
        )
        expected_response = {
            "status": 404,
            "status_text": "User not found"
        }
        self.assertEqual(self.client.login(**self.data), False)
        self.assertEqual(response.json(), expected_response)

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
        expected_response = {
            "status": 404,
            "status_text": "User not found"
        }
        self.assertEqual(self.client.login(**self.data), False)
        self.assertEqual(response.json(), expected_response)


class GetEmailApiTest(TestCase):
    def setUp(self) -> None:
        self.url_path = reverse("accounts:get-email")
        self.data = {
            "email": constants.EMAIL,
            "password": constants.PASSWORD
        }

    def test_get_email_with_authenticated_user(self):
        helper.create_user(**self.data)
        self.client.login(**self.data)

        response = self.client.get(path=self.url_path)
        expected_response = {
            "email": constants.EMAIL
        }
        self.assertEqual(expected_response, response.json())

    def test_get_email_with_unauthenticated_user(self):
        response = self.client.get(path=self.url_path)
        expected_response = {
            'detail': 'Authentication credentials were not provided.'
        }
        self.assertEqual(expected_response, response.json())
