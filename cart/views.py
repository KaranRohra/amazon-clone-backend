from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import views
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from cart import _private
from cart import models
from products import serializers as products_serializers


class GetProductFromCartApi(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = products_serializers.ProductSerializer

    def get_queryset(self, *args, **kwargs):
        cart = models.Cart.objects.get(user=self.request.user)
        return cart.products.all()


class AddProductApi(views.APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        product = _private.add_product_to_cart(user_email=request.user.email, product_id=kwargs["product_id"])
        if product:
            return Response(
                data={
                    "status": status.HTTP_201_CREATED,
                    "status_text": "Product added to cart",
                }
            )
        return Response(
            data={
                "status": status.HTTP_404_NOT_FOUND,
                "status_text": "Product not found",
            }
        )


class RemoveProductApi(views.APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        product = _private.remove_product_from_cart(user_email=request.user.email, product_id=kwargs["product_id"])
        if product:
            return Response(
                data={
                    "status": status.HTTP_200_OK,
                    "status_text": "Product removed from cart",
                }
            )
        return Response(
            data={
                "status": status.HTTP_404_NOT_FOUND,
                "status_text": "Product not found",
            }
        )
