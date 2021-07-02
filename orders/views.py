from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from accounts import models as accounts_models
from cart import public as cart_public
from orders import models
from orders import serializers


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
        products = cart_public.get_all_products_from_cart(user=request.user)
        address = accounts_models.Address.objects.get(pk=request.POST["address"])
        for product in products:
            product.quantity-=1
            models.Order.objects.create(
                user=request.user,
                address=address,
                product=product,
            )
            product.save()
        cart_public.remove_products_from_cart(user=request.user)
        return Response({"Order status": "Success"})

    def destroy(self, request, pk=None):
        return Response({"Order status": "Cannot delete"})
