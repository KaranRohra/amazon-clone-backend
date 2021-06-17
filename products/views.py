from rest_framework.response import Response
from rest_framework import generics
from rest_framework import views

from . import _private
from . import serializers
from . import models


class ProductApi(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        return Response(_private.get_products(kwargs["page_number"]))


class GetProductsApi(views.APIView):
    def get(self, request, *args, **kwargs):
        serialized_product = serializers.ProductSerializer(
            models.Product.objects.all(),
            many=True
        )
        return Response(serialized_product.data)

