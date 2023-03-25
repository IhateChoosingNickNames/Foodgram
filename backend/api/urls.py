from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register(r"recipes", views.RecipeViewset)
router_v1.register(r"tags", views.TagsViewset)
router_v1.register(r"ingredients", views.IngredientsViewset)

app_name = "api"

urlpatterns = [
    path("recipes/download_shopping_cart/", views.ShoppingCardView.as_view()),
    path(
        r"recipes/<int:recipe_id>/shopping_cart/",
        views.CreateDeleteShoppingCardView.as_view(),
    ),
    path(r"recipes/<int:recipe_id>/favorite/", views.FavoriteView.as_view()),
    path("", include(router_v1.urls)),
]
