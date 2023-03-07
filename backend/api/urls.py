from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter

router_v1 = SimpleRouter()
# router_v1.register()


app_name = "api"

urlpatterns = [
    path("v1/", include(router_v1.urls))
]