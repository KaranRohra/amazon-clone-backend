from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken import models as authtoken_models
from rest_framework.response import Response

from accounts import models, serializers


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


class GetUserAddresApi(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.AddressSerializer
    queryset = models.Address.objects.all()

    def list(self, request):
        user_address = serializers.AddressSerializer(models.Address.objects.filter(user=request.user), many=True).data
        return Response(user_address)
