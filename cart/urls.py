from django.urls import path

from cart import views

app_name = "cart"
urlpatterns = [
    path("create/", views.CreateCartApi.as_view(), name="create"),
    path("get-products/", views.GetProductFromCartApi.as_view(), name="get-products"),
    path("add-product/<int:product_id>/", views.AddProductApi.as_view(), name="add-product"),
    path("remove-product/<int:product_id>/", views.RemoveProductApi.as_view(), name="remove-product"),
]
