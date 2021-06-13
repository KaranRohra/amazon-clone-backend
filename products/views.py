from rest_framework.response import Response
from rest_framework import generics

from . import _private


class ProductApi(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        return Response(_private.get_products(kwargs["page_number"]))
