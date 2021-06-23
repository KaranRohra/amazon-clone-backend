from rest_framework import generics
from rest_framework import viewsets

from django.db import models as db_models

from products import _private
from products import serializers
from products import models


class ProductsApi(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        return _private.get_products(self.kwargs["page_number"])


class ImageApi(generics.RetrieveAPIView):
    serializer_class = serializers.ProductImageSerializer
    queryset = models.ProductImage.objects.all()
    lookup_field = "id"


class ProductApi(viewsets.ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()


class ProductSearchApi(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    model = models.Product

    def get_queryset(self):
        search_string = self.request.GET.get("search", "")
        query_set = self.model.objects.filter(
            db_models.Q(name__icontains=search_string) | 
            db_models.Q(category__icontains=search_string)
        )
        return query_set if query_set else models.Product.objects.all()
