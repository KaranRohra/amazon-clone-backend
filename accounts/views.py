from rest_framework import status
from rest_framework import parsers
from rest_framework import views
from rest_framework.response import Response

from django.contrib import auth
from django.http import JsonResponse

from . import _private


class CreateUserAccountApi(views.APIView):
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    def post(self, request):
        user = _private.create_user_account(request.data)
        if user:
            _private.login_user(request)
            return Response({"status": status.HTTP_201_CREATED})
        return Response({"status": status.HTTP_400_BAD_REQUEST})


class LoginApi(views.APIView):
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    def post(self, request):
        user = _private.login_user(request)
        if user:
            return Response({"status": status.HTTP_200_OK})
        return Response({"status": status.HTTP_404_NOT_FOUND})


def get_email_api(request):
    if request.user.is_authenticated:
        return JsonResponse({"email": request.user.email})
    return JsonResponse({})


def logout_api(request):
    auth.logout(request)
    return JsonResponse({})
