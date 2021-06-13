from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("get-product-by-page-number/<int:page_number>/", views.ProductApi.as_view(),
         name="get-product-by-page-number"),
    path("save-product/", views.ProductApi.as_view(), name="save-product"),
]
