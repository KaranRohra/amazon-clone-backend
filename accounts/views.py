from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken import models as authtoken_models
from rest_framework.response import Response

from accounts import models
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
        return Response(serializers.UserSerializer(request.user).data)


class UserAddressApi(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.AddressSerializer
    queryset = models.Address.objects.all()

    def get_queryset(self, *args, **kwargs):
        return models.Address.objects.filter(user=self.request.user, is_address_deleted=False)

    def create(self, request, *args, **kwargs):
        models.Address.objects.create(**request.POST.dict(), user=request.user)
        return Response({"Address save": "Success"}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        address = get_object_or_404(models.Address, pk=kwargs["pk"], is_address_deleted=False, user=request.user)
        address.is_address_deleted = True
        address.save()
        return Response({"Address delete": "Success"})
