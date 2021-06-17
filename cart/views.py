from rest_framework import views
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from . import _private
from . import models


class CreateCartApi(views.APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        models.Cart.objects.create(user=request.user)
        return Response({
            "status": status.HTTP_201_CREATED,
            "status_text": f"Cart created for user {request.user.email}"
        })


class GetProductFromCartApi(views.APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        products = _private.get_product_from_cart(
            user_email=request.user.email
        )
        return Response(products)


class AddProductApi(views.APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        product = _private.add_product_to_cart(
            user_email=request.user.email,
            product_id=kwargs["product_id"]
        )
        if product:
            return Response(data={
                "status": status.HTTP_201_CREATED,
                "status_text": "Product added to cart",
            })
        return Response(data={
                "status": status.HTTP_404_NOT_FOUND,
                "status_text": "Product not found",
            })


class RemoveProductApi(views.APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        product = _private.remove_product_from_cart(
            user_email=request.user.email,
            product_id=kwargs["product_id"]
        )
        if product:
            return Response(data={
                "status": status.HTTP_200_OK,
                "status_text": "Product removed from cart",
            })
        return Response(data={
            "status": status.HTTP_404_NOT_FOUND,
            "status_text": "Product not found",
        })
