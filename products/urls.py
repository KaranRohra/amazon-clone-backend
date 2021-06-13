from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("get-product-by-range/<int:range>/", views.ProductApi.as_view(), name="get-product-by-range"),
    path("save-product/", views.ProductApi.as_view(), name="save-product"),
]
