from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from accounts import views

app_name = "accounts"

router = routers.DefaultRouter()
router.register("user/address", views.GetUserAddresApi, basename="address")


urlpatterns = [
    path("get-user/", views.GetUserApi.as_view(), name="get-user"),
    path("logout/", views.LogoutApi.as_view(), name="logout"),
    path("register/", views.RegisterApi.as_view(), name="register"),
    path("auth/", obtain_auth_token, name="auth"),
] + router.urls
