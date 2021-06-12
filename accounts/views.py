from rest_framework import status
from rest_framework import parsers
from rest_framework import views
from rest_framework.response import Response

from . import _private


class CreateUserAccountApi(views.APIView):
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    def post(self, request):
        user = _private.create_user_account(request.data)
        if user:
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginApi(views.APIView):
    parser_classes = [parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser]

    def post(self, request):
        user = _private.get_user(
            email=request.data["email"],
            password=request.data["password"]
        )
        if user:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
