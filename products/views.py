from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from products import _private
from products import models
from products import serializers


class ProductsPageNumberApi(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        return _private.get_products(
            page_number=self.kwargs["page_number"],
            search_by=self.request.GET.get("search", ""),
        )


class ProductApi(viewsets.ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()


@api_view(("GET",))
def get_products_count(request):
    number_of_products = _private.get_products_count_based_on_search_value(request.GET.get("search", ""))
    return Response(number_of_products)
