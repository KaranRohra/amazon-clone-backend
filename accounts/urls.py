from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("get-email/", views.get_email_api, name="get-email"),
    path("logout/", views.logout_api, name="logout"),
    path("create/", views.CreateUserAccountApi.as_view(), name="create-user"),
    path("login/", views.LoginApi.as_view(), name="login-user"),
]
