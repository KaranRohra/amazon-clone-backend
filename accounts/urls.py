from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = "accounts"

urlpatterns = [
    path("get-user/", views.GetUserApi.as_view(), name="get-email"),
    path("logout/", views.LogoutApi.as_view(), name="logout"),
    path("register/", views.RegisterApi.as_view(), name="register"),
    path("auth/", obtain_auth_token, name="auth"),
]
