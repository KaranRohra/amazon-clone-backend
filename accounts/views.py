from rest_framework import status
from rest_framework.authtoken import models as authtoken_models
from rest_framework import views
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics

from accounts import serializers


class RegisterApi(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


class LogoutApi(views.APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        authtoken_models.Token.objects.get(user__email=request.user).delete()
        return Response({"status": status.HTTP_200_OK, "status_text": "Logout success"})


class GetUserApi(views.APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        request.session.flush()
        return Response(serializers.UserSerializer(request.user).data)
