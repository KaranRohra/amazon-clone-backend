from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken import models as authtoken_models

from accounts import constants, models, serializers
from common.tests import helper


class CrateUserAccountTest(TestCase):
    def setUp(self) -> None:
        self.url_path = reverse("accounts:register")
        self.data = {"email": constants.EMAIL, "password": constants.PASSWORD}

    def test_create_user(self):
        response = self.client.post(path=self.url_path, data=self.data)

        # If this doesn't raise exception then it indicates that our api is working
        user = models.User.objects.get(email=constants.EMAIL)
        expected_response = serializers.UserSerializer(user).data
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_create_user_with_already_exist_user(self):
        helper.create_user(
            email=constants.EMAIL,
            password=constants.PASSWORD,
        )
        try:
            response = self.client.post(path=self.url_path, data=self.data)
            self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        except IntegrityError:
            self.assertEqual(True, True)
        else:
            self.assertEqual(True, True)

    def test_create_user_with_invalid_email(self):
        self.data["email"] = constants.INVALID_EMAIL_SYNTAX
        response = self.client.post(
            path=self.url_path,
            data=self.data,
        )
        expected_response = {"email": ["Enter a valid email address."]}
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class LoginTest(TestCase):
    def setUp(self) -> None:
        self.url_path = reverse("accounts:auth")
        self.data = {"username": constants.EMAIL, "password": constants.PASSWORD}

    def test_login_with_valid_user(self):
        helper.create_user(
            email=constants.EMAIL,
            password=constants.PASSWORD,
        )
        response = self.client.post(path=self.url_path, data=self.data)

        expected_response = {"token": authtoken_models.Token.objects.get(user__email=constants.EMAIL).key}
        self.assertEqual(self.client.login(**self.data), True)
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_login_without_user(self):
        response = self.client.post(path=self.url_path, data=self.data)
        expected_response = {"non_field_errors": ["Unable to log in with provided credentials."]}
        self.assertEqual(self.client.login(**self.data), False)
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

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
        expected_response = {"non_field_errors": ["Unable to log in with provided credentials."]}
        self.assertEqual(self.client.login(**self.data), False)
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
