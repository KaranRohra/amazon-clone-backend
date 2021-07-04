from rest_framework.authtoken import models as authtoken_models
from rest_framework import status
from rest_framework import test

from django.urls import reverse
from django.utils import timezone

from accounts import models
from accounts import serializers
from common.tests import helper
from common.tests import constants


class CrateUserAccountTest(test.APITestCase):
    def setUp(self) -> None:
        self.url_path = reverse("accounts:register")
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
        user = models.User.objects.get(email=constants.EMAIL)
        expected_response = serializers.UserSerializer(user).data
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

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
            "email": ["user with this email already exists."]
        }
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(expected_response, response.json())

    def test_create_user_with_invalid_email(self):
        self.data["email"] = constants.INVALID_EMAIL_SYNTAX
        response = self.client.post(
            path=self.url_path,
            data=self.data,
        )
        expected_response = {
            "email": ["Enter a valid email address."]
        }
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class LoginTest(test.APITestCase):
    def setUp(self) -> None:
        self.url_path = reverse("accounts:auth")
        self.user_info = {
            "username": constants.EMAIL,
            "password": constants.PASSWORD
        }

    def test_login_with_valid_user(self):
        helper.create_user(
            email=constants.EMAIL,
            password=constants.PASSWORD,
        )
        response = self.client.post(
            path=self.url_path,
            data=self.user_info
        )

        expected_response = {
            "token": authtoken_models.Token.objects.get(user__email=constants.EMAIL).key
        }
        self.assertEqual(self.client.login(**self.user_info), True)
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_login_without_user(self):
        response = self.client.post(
            path=self.url_path,
            data=self.user_info
        )
        expected_response = {
            "non_field_errors": ["Unable to log in with provided credentials."]
        }
        self.assertEqual(self.client.login(**self.user_info), False)
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_login_with_invalid_password(self):
        helper.create_user(
            email=constants.EMAIL,
            password=constants.PASSWORD,
        )
        self.user_info["password"] = "wrong password"
        response = self.client.post(
            path=self.url_path,
            data=self.user_info,
        )
        expected_response = {
            "non_field_errors": ["Unable to log in with provided credentials."]
        }
        self.assertEqual(self.client.login(**self.user_info), False)
        self.assertEqual(response.json(), expected_response)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class GetUserApiTest(test.APITestCase):
    def setUp(self) -> None:
        self.url_path = reverse("accounts:get-user")
        self.client = test.APIClient()
        self.user_info = {
            "email": constants.EMAIL,
            "password": constants.PASSWORD,
            "first_name": constants.FIRST_NAME,
            "last_name": constants.LAST_NAME,
        }
    
    def test_get_user_with_user(self):
        user = helper.create_user(**self.user_info)
        token = helper.generate_token(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = self.client.get(self.url_path)
        expected_response = {
            "id": user.id,
            "email": constants.EMAIL,
            "first_name": constants.FIRST_NAME,
            "last_name": constants.LAST_NAME,
            "is_active": True,
            "date_joined": str(timezone.localtime(user.date_joined)).replace(" ", "T"),
            "last_login": None,
        }
        self.assertEqual(expected_response, response.json())
        self.assertEqual(status.HTTP_200_OK, response.status_code)
    
    def test_get_user_with_invalid_token(self):
        helper.create_user(**self.user_info)
        self.client.credentials(HTTP_AUTHORIZATION="Token InvalidToken")
        response = self.client.get(self.url_path)
        expected_response = {
           "detail": "Invalid token."
        }
        self.assertEqual(expected_response, response.json())
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
    
    def test_get_user_with_invalid_token(self):
        helper.create_user(**self.user_info)
        response = self.client.get(self.url_path)
        expected_response = {'detail': 'Authentication credentials were not provided.'}
        self.assertEqual(expected_response, response.json())
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class UserAddressApiTestCase(test.APITestCase):
    def setUp(self):
        self.client = test.APIClient()
        self.list_api_url = reverse("accounts:address-list")
        self.user_info = {
            "email": constants.EMAIL,
            "password": constants.PASSWORD,
        }
    
    def test_user_address_with_valid_user(self):
        user = helper.create_user(**self.user_info)
        address_list = helper.create_address(user=user, number_of_address=5)
        expected_response = serializers.AddressSerializer(address_list, many=True).data

        token = helper.generate_token(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = self.client.get(self.list_api_url)
        
        
        self.assertEqual(expected_response, response.json())
        self.assertEqual(status.HTTP_200_OK, response.status_code)
    
    def test_user_addess_without_address(self):
        user = helper.create_user(**self.user_info)
        expected_response = []

        token = helper.generate_token(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = self.client.get(self.list_api_url)
        
        
        self.assertEqual(expected_response, response.json())
        self.assertEqual(status.HTTP_200_OK, response.status_code)
    
    def test_user_addess_without_token(self):
        helper.create_user(**self.user_info)
        expected_response = {'detail': 'Authentication credentials were not provided.'}

        response = self.client.get(self.list_api_url)
        
        self.assertEqual(expected_response, response.json())
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
    
    def test_user_addess_with_invalid_token(self):
        helper.create_user(**self.user_info)
        self.client.credentials(HTTP_AUTHORIZATION="Token InvalidToken")
        expected_response = {
           "detail": "Invalid token."
        }

        response = self.client.get(self.list_api_url)
        
        self.assertEqual(expected_response, response.json())
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
    
    def test_user_address_save_address(self):
        user = helper.create_user(**self.user_info)
        constants.ADDRESS["user"] = user.id
        constants.ADDRESS["id"] = 1  # Since we are creating only one address object so id is 1

        token = helper.generate_token(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        response = self.client.post(
            self.list_api_url, 
            data=constants.ADDRESS
        )
        
        self.assertEqual(constants.ADDRESS, response.json())
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
