from rest_framework import routers, urlpatterns

from orders import views


router = routers.DefaultRouter()
router.register("", views.OrdersApi)


urlpatterns = [] + router.urls
