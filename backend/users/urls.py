from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "users"

users_router_v1 = DefaultRouter()
users_router_v1.register("users", views.UserViewSet)


urlpatterns = [
    path(r"users/subscriptions/", views.SubscribeListView.as_view()),
    path(r"", include(users_router_v1.urls)),
    path(r"auth/", include("djoser.urls.authtoken")),
    path(r"users/<int:user_id>/subscribe/", views.SubscribeView.as_view()),
]
