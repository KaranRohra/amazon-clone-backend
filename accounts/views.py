from rest_framework import status
from rest_framework import parsers
from rest_framework import views
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import decorators

from django.contrib import auth
from django.http import JsonResponse

from . import _private


class CreateUserAccountApi(views.APIView):
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    def post(self, request):
        response = {
            "status": status.HTTP_406_NOT_ACCEPTABLE,
            "status_text": "Invalid email"
        }

        # This condition helps to validate email if email is not proper then return 406
        if not _private.is_email_valid(request.data["email"]):
            return Response(response)

        user = _private.create_user_account(request.data)
        if user:
            response["status"] = status.HTTP_201_CREATED
            response["status_text"] = "Account created successfully"
            _private.login_user(request)
            return Response(response)

        response["status"] = status.HTTP_400_BAD_REQUEST
        response["status_text"] = "Account already exist"
        return Response(response)


class LoginApi(views.APIView):
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    def post(self, request):
        user = _private.login_user(request)
        response = {
            "status": status.HTTP_200_OK,
            "status_text": "Login successfully"
        }
        if user:
            return Response(response)

        response["status"] = status.HTTP_404_NOT_FOUND  # indicating user not found
        response["status_text"] = "User not found"
        return Response(response)


@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.IsAuthenticated])
def get_email_api(request):
    if request.user.is_authenticated:
        return JsonResponse({"email": request.user.email})
    return JsonResponse({})


@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.IsAuthenticated])
def logout_api(request):
    auth.logout(request)
    return JsonResponse({})
