from django.urls import path
from rest_framework import routers

from products import views

app_name = "products"
router = routers.DefaultRouter()
router.register("", views.ProductApi, basename="product")

urlpatterns = [
    path(
        "page-number/<int:page_number>/",
        views.ProductsPageNumberApi.as_view(),
        name="page-number",
    ),
    path("count/", views.get_products_count, name="count"),
] + router.urls
