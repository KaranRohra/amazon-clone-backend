from rest_framework import routers

from django.urls import path

from products import views

app_name = "products"
router = routers.DefaultRouter()
router.register("", views.ProductApi, basename="product")

urlpatterns = [
    path("get-product-by-page-number/<int:page_number>/", views.ProductsApi.as_view(),
         name="get-product-by-page-number"),
    path("image/<int:id>/", views.ImageApi.as_view(), name="get-image")
] + router.urls
