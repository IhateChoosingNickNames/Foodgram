import django_filters

from django_filters import rest_framework as filters
from recipes.models import Recipe, Favorite, Tag, ShoppingCard, Ingredient


class RecipeSearchFilter(django_filters.FilterSet):
    """Фильтрация рецептов."""

    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name="tags__slug",
        to_field_name="slug",
    )
    ingredients = filters.CharFilter(field_name="ingredients__name")
    is_favorited = filters.BooleanFilter(
        field_name="is_favorited", method="filter_is_favorited"
    )
    author = filters.CharFilter(field_name="author__id")
    is_in_shopping_cart = filters.BooleanFilter(
        field_name="is_in_shopping_cart", method="filter_is_in_shopping_cart"
    )

    def filter_is_favorited(self, queryset, name, value):

        if value:
            return queryset.filter(
                id__in=Favorite.objects.filter(user=self.request.user).values(
                    "recipe_id"
                )
            )

        return queryset.exclude(
            id__in=Favorite.objects.filter(user=self.request.user).values(
                "recipe_id"
            )
        )

    def filter_is_in_shopping_cart(self, queryset, name, value):

        if value:
            return queryset.filter(
                id__in=ShoppingCard.objects.filter(
                    user=self.request.user
                ).values("recipe_id")
            )

        return queryset.exclude(
            id__in=ShoppingCard.objects.filter(user=self.request.user).values(
                "recipe_id"
            )
        )

    class Meta:
        model = Recipe
        fields = (
            "tags",
            "ingredients",
            "is_favorited",
            "author",
            "is_in_shopping_cart",
        )


class IngredientSearchFilter(filters.FilterSet):
    """Фильтрация ингредиентов."""

    name = filters.CharFilter(field_name="name", method="filter_name")

    class Meta:
        model = Ingredient
        fields = ("name",)

    @staticmethod
    def filter_name(queryset, name, value):
        return queryset.filter(name__icontains=value.lower())
