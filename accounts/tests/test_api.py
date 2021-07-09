from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework import test
from rest_framework.authtoken import models as authtoken_models

from accounts import models
from accounts import serializers
from accounts.tests import constants as accounts_constants
from accounts.tests import helper


class CrateUserAccountTest(test.APITestCase):
    def setUp(self) -> None:
        self.url_path = reverse("accounts:register")

    def test_create_user(self):
        response = self.client.post(path=self.url_path, data=accounts_constants.USER_INFO)

        # If this doesn't raise exception then it indicates that our api is working
        user = models.User.objects.get(email=accounts_constants.EMAIL)
        expected_response = serializers.UserSerializer(user).data
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_create_user_with_already_exist_user(self):
        helper.User()
        response = self.client.post(path=self.url_path, data=accounts_constants.USER_INFO)
        expected_response = {"email": ["user with this email already exists."]}
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(expected_response, response.json())

    def test_create_user_with_invalid_email(self):
        response = self.client.post(
            path=self.url_path,
            data=accounts_constants.USER_INVALID_INFO,
        )
        expected_response = {"email": ["Enter a valid email address."]}
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class LoginTest(test.APITestCase):
    def setUp(self) -> None:
        self.user_info = {
            "username": accounts_constants.EMAIL,
            "password": accounts_constants.PASSWORD,
        }
        self.user_object = helper.User()
        self.url_path = reverse("accounts:auth")

    def test_login_with_valid_user(self):
        response = self.client.post(path=self.url_path, data=self.user_info)

        expected_response = {"token": authtoken_models.Token.objects.get(user__email=accounts_constants.EMAIL).key}
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
            "email": accounts_constants.EMAIL,
            "password": accounts_constants.PASSWORD,
            "first_name": accounts_constants.FIRST_NAME,
            "last_name": accounts_constants.LAST_NAME,
        }

    def test_get_user_with_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_object.user_1_token}")
        response = self.client.get(self.url_path)
        expected_response = {
            "id": self.user.id,
            "email": accounts_constants.EMAIL,
            "first_name": accounts_constants.FIRST_NAME,
            "last_name": accounts_constants.LAST_NAME,
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
        self.user_2 = self.user_object.user_2

        self.client = test.APIClient()
        self.list_api_url = reverse("accounts:address-list")
        self.address_id_1 = 1
        self.address_detail_api_url = reverse("accounts:address-detail", kwargs={"pk": self.address_id_1})

    def test_user_address_with_valid_user(self):
        expected_response = serializers.AddressSerializer(self.user_object.user_1_address, many=True).data

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_object.user_1_token}")
        response = self.client.get(self.list_api_url)

        self.assertEqual(expected_response, response.json())
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_address_without_address(self):
        expected_response = []

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_object.user_2_token}")
        response = self.client.get(self.list_api_url)

        self.assertEqual(expected_response, response.json())
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_address_without_token(self):
        expected_response = {"detail": "Authentication credentials were not provided."}

        response = self.client.get(self.list_api_url)

        self.assertEqual(expected_response, response.json())
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_user_address_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token InvalidToken")
        expected_response = {"detail": "Invalid token."}

        response = self.client.get(self.list_api_url)

        self.assertEqual(expected_response, response.json())
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_user_address_save_address(self):
        # We are doing total count + 1, because if new address is added then count of address is increased by 1
        accounts_constants.ADDRESS["id"] = models.Address.objects.count() + 1

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_object.user_2_token}")
        response = self.client.post(self.list_api_url, data=accounts_constants.ADDRESS)

        expected_response = {
            "Address save": "Success",
            "id": accounts_constants.ADDRESS["id"],
        }

        self.assertEqual(expected_response, response.json())
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        accounts_constants.ADDRESS.pop("id")

    def test_delete_user_address(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_object.user_1_token}")
        response = self.client.delete(self.address_detail_api_url)

        expected_response = {"Address delete": "Success"}

        self.assertTrue(models.Address.objects.get(pk=self.address_id_1).is_address_deleted)
        self.assertEqual(expected_response, response.json())
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_delete_user_address_which_is_not_belong_to_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_object.user_2_token}")
        response = self.client.delete(self.address_detail_api_url)

        expected_response = {"detail": "Not found."}

        self.assertEqual(expected_response, response.json())
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class LogoutUserApi(test.APITestCase):
    def setUp(self) -> None:
        self.user_object = helper.User()
        self.logout_url = reverse("accounts:logout")
        self.client = test.APIClient()

    def test_logout_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_object.user_1_token}")
        response = self.client.get(self.logout_url)
        expected_response = {"status": status.HTTP_200_OK, "status_text": "Logout success"}
        self.assertEqual(expected_response, response.json())

    def test_logout_without_token(self):
        response = self.client.get(self.logout_url)
        expected_response = {"detail": "Authentication credentials were not provided."}
        self.assertEqual(expected_response, response.json())
