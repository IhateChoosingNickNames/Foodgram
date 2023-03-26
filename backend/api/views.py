from django.db.models import Exists, OuterRef
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCard, Tag
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     RetrieveAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from api.filters import IngredientSearchFilter, RecipeSearchFilter
from api.pagination import CustomPagination
from api.permissions import (IsAdminOrReadOnly, IsAuthorOrReadOnly,
                             IsNotBlockedOrReadOnly)
from api.serializers import (FavoriteSerializer, IngredientsSerializer,
                             RecipeReadSerializer, RecipeWriteSerializer,
                             ShoppingCardSerializer, TagsSerializer)
from api.utils import pdf_response_creator


class RecipeViewset(ModelViewSet):
    """Вьюсет рецептов."""

    queryset = (
        Recipe.objects.select_related("author")
        .prefetch_related("ingredients", "tags")
        .annotate(
            is_in_shopping_cart=Exists(
                ShoppingCard.objects.filter(recipe=OuterRef("pk"))
            ),
            is_favorited=Exists(
                Favorite.objects.filter(recipe=OuterRef("pk"))
            ),
        )
    )

    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeSearchFilter
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
        IsNotBlockedOrReadOnly,
    )

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RecipeReadSerializer
        return RecipeWriteSerializer


class TagsViewset(ModelViewSet):
    """Вьюсет тегов."""

    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer


class IngredientsViewset(ModelViewSet):
    """Вьюсет ингредиентов."""

    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientSearchFilter


class ShoppingCardView(RetrieveAPIView):
    """Получение корзины в виде файла."""

    permission_classes = (IsNotBlockedOrReadOnly,)
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

    permission_classes = (IsNotBlockedOrReadOnly, IsNotBlockedOrReadOnly)
    serializer_class = ShoppingCardSerializer

    def get_object(self):
        return get_object_or_404(Recipe, id=self.kwargs["recipe_id"])

    def perform_create(self, serializer):
        serializer.save(
            user_id=self.request.user.id, recipe_id=self.get_object().id
        )

    def perform_destroy(self, instance):
        to_delete = get_object_or_404(
            ShoppingCard, user_id=self.request.user.id, recipe_id=instance.id
        )
        to_delete.delete()


class FavoriteView(CreateAPIView, DestroyAPIView):
    """Добавление и удаление рецептов в избранное."""

    permission_classes = (IsNotBlockedOrReadOnly, IsNotBlockedOrReadOnly)
    serializer_class = FavoriteSerializer

    def get_object(self):
        return get_object_or_404(
            Recipe, id=self.request.parser_context["kwargs"]["recipe_id"]
        )

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        Favorite.objects.create(
            user=self.request.user, recipe=self.get_object()
        )

    def perform_destroy(self, instance):
        get_object_or_404(
            Favorite, user=self.request.user, recipe=self.get_object()
        ).delete()
