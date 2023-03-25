from collections import defaultdict


from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    RetrieveAPIView,
    DestroyAPIView,
    CreateAPIView,
)
from api.filters import RecipeSearchFilter, IngredientSearchFilter
from api.pagination import CustomPagination
from api.serializers import (
    TagsSerializer,
    IngredientsSerializer,
    ShoppingCardSerializer,
    FavoriteSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
)
from api.utils import pdf_response_creator
from recipes.models import Recipe, Tag, Ingredient, ShoppingCard, Favorite
from django_filters.rest_framework import DjangoFilterBackend


class RecipeViewset(ModelViewSet):
    """Вьюсет рецептов."""

    queryset = Recipe.objects.select_related("author").prefetch_related(
        "ingredients", "tags"
    )

    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeSearchFilter

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RecipeReadSerializer
        return RecipeWriteSerializer


class TagsViewset(ModelViewSet):
    """Вьюсет тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagsSerializer


class IngredientsViewset(ModelViewSet):
    """Вьюсет ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientSearchFilter


class ShoppingCardView(RetrieveAPIView):
    """Получение корзины в виде файла."""

    serializer_class = ShoppingCardSerializer

    def get_object(self):
        return self.request.user.id

    def get_queryset(self):
        return ShoppingCard.objects.filter(user__id=self.get_object())

    def retrieve(self, request, *args, **kwargs):

        data = {}

        for recipe in self.get_queryset():
            for rec_ingr in recipe.recipe.recipe_ingr.all():
                curr_ingredient = rec_ingr.ingredient
                if curr_ingredient.name not in data:
                    data[curr_ingredient.name] = {
                        "amount": 0,
                        "measurement_unit": curr_ingredient.measurement_unit,
                    }
                data[curr_ingredient.name]["amount"] += rec_ingr.amount

        return pdf_response_creator(data)


class CreateDeleteShoppingCardView(DestroyAPIView, CreateAPIView):
    """Добавление и удаление рецептов в корзину."""

    serializer_class = ShoppingCardSerializer

    def get_object(self):
        return Recipe.objects.get(id=self.kwargs["recipe_id"])

    def perform_create(self, serializer):
        serializer.save(
            user_id=self.request.user.id, recipe_id=self.get_object().id
        )

    def perform_destroy(self, instance):
        to_delete = ShoppingCard.objects.get(
            user_id=self.request.user.id, recipe_id=instance.id
        )
        to_delete.delete()


class FavoriteView(CreateAPIView, DestroyAPIView):
    """Добавление и удаление рецептов в избранное."""

    serializer_class = FavoriteSerializer

    def get_object(self):
        return Recipe.objects.get(
            id=self.request.parser_context["kwargs"]["recipe_id"]
        )

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        Favorite.objects.create(
            user=self.request.user, recipe=self.get_object()
        )

    def perform_destroy(self, instance):
        Favorite.objects.get(
            user=self.request.user, recipe=self.get_object()
        ).delete()
