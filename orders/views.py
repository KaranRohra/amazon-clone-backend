from rest_framework import permissions, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from orders import _private, models, serializers


class OrdersApi(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.OrderSerializer
    queryset = models.Order.objects.all()

    def list(self, request):
        orders = serializers.OrderSerializer(
            models.Order.objects.filter(user=request.user),
            many=True,
        ).data
        return Response(orders)

    def create(self, request):
        try:
            _private.place_order(user=request.user, address=request.POST["address"])
            response = {"Order status": "Success"}
        except Exception as e:
            response = {"error": str(e)}
        return Response(response)

    def destroy(self, request, pk=None):
        return Response({"Order status": "Cannot delete"})
