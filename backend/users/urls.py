from django.urls import include, path

from . import views

app_name = "users"

urlpatterns = [
    path(r"users/subscriptions/", views.SubscribeListView.as_view()),
    path(r"", include("djoser.urls")),
    path(r"auth/", include("djoser.urls.authtoken")),
    path(r"users/<int:user_id>/subscribe/", views.SubscribeView.as_view()),
]
