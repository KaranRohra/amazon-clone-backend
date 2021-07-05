from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework import test
from rest_framework.authtoken import models as authtoken_models

from accounts import models
from accounts import serializers
from accounts.tests import helper
from common.tests import constants as common_constants
from common.tests import helper as common_helper


class CrateUserAccountTest(test.APITestCase):
    def setUp(self) -> None:
        self.url_path = reverse("accounts:register")

    def test_create_user(self):
        response = self.client.post(path=self.url_path, data=common_constants.USER_INFO)

        # If this doesn't raise exception then it indicates that our api is working
        user = models.User.objects.get(email=common_constants.EMAIL)
        expected_response = serializers.UserSerializer(user).data
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_create_user_with_already_exist_user(self):
        helper.User()
        response = self.client.post(path=self.url_path, data=common_constants.USER_INFO)
        expected_response = {"email": ["user with this email already exists."]}
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(expected_response, response.json())

    def test_create_user_with_invalid_email(self):
        response = self.client.post(
            path=self.url_path,
            data=common_constants.USER_INVALID_INFO,
        )
        expected_response = {"email": ["Enter a valid email address."]}
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class LoginTest(test.APITestCase):
    def setUp(self) -> None:
        self.user_info = {
            "username": common_constants.EMAIL,
            "password": common_constants.PASSWORD,
        }
        self.user_object = helper.User()
        self.url_path = reverse("accounts:auth")

    def test_login_with_valid_user(self):
        response = self.client.post(path=self.url_path, data=self.user_info)

        expected_response = {"token": authtoken_models.Token.objects.get(user__email=common_constants.EMAIL).key}
        self.assertEqual(self.client.login(**self.user_info), True)
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_login_without_user(self):
        self.user_object.delete_user(self.user_object.user_1)
        response = self.client.post(path=self.url_path, data=self.user_info)
        expected_response = {"non_field_errors": ["Unable to log in with provided credentials."]}
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_login_with_invalid_password(self):
        self.user_info["password"] = "wrong password"
        response = self.client.post(
            path=self.url_path,
            data=self.user_info,
        )
        expected_response = {"non_field_errors": ["Unable to log in with provided credentials."]}
        self.assertEqual(self.client.login(**self.user_info), False)
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class GetUserApiTest(test.APITestCase):
    def setUp(self) -> None:
        self.user_object = helper.User()
        self.user = self.user_object.user_1
        self.url_path = reverse("accounts:get-user")
        self.client = test.APIClient()
        self.user_info = {
            "email": common_constants.EMAIL,
            "password": common_constants.PASSWORD,
            "first_name": common_constants.FIRST_NAME,
            "last_name": common_constants.LAST_NAME,
        }

    def test_get_user_with_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_object.user_1_token}")
        response = self.client.get(self.url_path)
        expected_response = {
            "id": self.user.id,
            "email": common_constants.EMAIL,
            "first_name": common_constants.FIRST_NAME,
            "last_name": common_constants.LAST_NAME,
            "is_active": True,
            "date_joined": str(timezone.localtime(self.user.date_joined)).replace(" ", "T"),
            "last_login": None,
        }
        self.assertEqual(expected_response, response.json())
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_user_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token InvalidToken")
        response = self.client.get(self.url_path)
        expected_response = {"detail": "Invalid token."}
        self.assertEqual(expected_response, response.json())
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_user_without_token(self):
        response = self.client.get(self.url_path)
        expected_response = {"detail": "Authentication credentials were not provided."}
        self.assertEqual(expected_response, response.json())
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class UserAddressApiTestCase(test.APITestCase):
    def setUp(self):
        self.user_object = helper.User()
        self.user_1 = self.user_object.user_1

        self.client = test.APIClient()
        self.list_api_url = reverse("accounts:address-list")

    def test_user_address_with_valid_user(self):
        address_list = common_helper.create_address(user=self.user_1, number_of_address=5)
        expected_response = serializers.AddressSerializer(address_list, many=True).data

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_object.user_1_token}")
        response = self.client.get(self.list_api_url)

        self.assertEqual(expected_response, response.json())
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_addess_without_address(self):
        expected_response = []

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_object.user_1_token}")
        response = self.client.get(self.list_api_url)

        self.assertEqual(expected_response, response.json())
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_addess_without_token(self):
        expected_response = {"detail": "Authentication credentials were not provided."}

        response = self.client.get(self.list_api_url)

        self.assertEqual(expected_response, response.json())
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_user_addess_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token InvalidToken")
        expected_response = {"detail": "Invalid token."}

        response = self.client.get(self.list_api_url)

        self.assertEqual(expected_response, response.json())
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_user_address_save_address(self):
        common_constants.ADDRESS["user"] = self.user_1.id
        common_constants.ADDRESS["id"] = 1  # Since we are creating only one address object so id is 1

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_object.user_1_token}")
        response = self.client.post(self.list_api_url, data=common_constants.ADDRESS)

        self.assertEqual(common_constants.ADDRESS, response.json())
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
