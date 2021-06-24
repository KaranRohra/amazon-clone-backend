from rest_framework import generics
from rest_framework import viewsets

from django.db import models as db_models

from products import _private
from products import serializers
from products import models


class ProductsPageNumberApi(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        return _private.get_products(
            page_number=self.kwargs["page_number"], 
            search_by=self.request.GET.get("search", "")
        )

class ProductApi(viewsets.ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
