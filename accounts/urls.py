from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("create/", views.CreateUserAccountApi.as_view(), name="create-user"),
    path("login/", views.LoginApi.as_view(), name="login-user"),
]
