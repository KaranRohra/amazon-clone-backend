from rest_framework import generics
from rest_framework import viewsets

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
