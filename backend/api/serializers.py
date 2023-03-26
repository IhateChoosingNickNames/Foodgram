import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCard, Tag)
from users.serializers import CustomUserSerializer


class Base64ImageField(serializers.ImageField):
    """Декодирование Base64 в файл."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, encoded_image = data.split(";base64,")
            extension = format.split("/")[-1]
            data = ContentFile(
                base64.b64decode(encoded_image), name="image." + extension
            )

        return super().to_internal_value(data)


class TagsSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")

    def to_internal_value(self, data):
        return Tag.objects.get(id=data)


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    """Сериализатор добавления поля amount в модель ингредиентов.
    Только для записи.
    """

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ("id", "amount")

    def to_representation(self, instance):
        if "amount" in self.fields:
            self.fields.pop("amount")
        return super().to_representation(instance)


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения игредиента и соответствующего ему amount."""

    id = serializers.PrimaryKeyRelatedField(
        source="ingredient", read_only=True
    )
    name = serializers.SlugRelatedField(
        slug_field="name", source="ingredient", read_only=True
    )
    measurement_unit = serializers.SlugRelatedField(
        slug_field="measurement_unit", source="ingredient", read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "name", "measurement_unit", "amount")


class BaseRecipeSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для рецептов."""

    author = CustomUserSerializer(default=serializers.CurrentUserDefault())
    image = Base64ImageField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    tags = TagsSerializer(many=True)

    def get_is_in_shopping_cart(self, obj):
        if self.context["request"].user.is_authenticated:
            return obj.is_in_shopping_cart
        return False

    def get_is_favorited(self, obj):
        if self.context["request"].user.is_authenticated:
            return obj.is_favorited
        return False


class RecipeReadSerializer(BaseRecipeSerializer):
    """Сериализатор рецептов(чтение)."""

    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
            "is_in_shopping_cart",
            "is_favorited",
        )
        read_only_fields = ("author",)

    def get_ingredients(self, obj):
        return RecipeIngredientReadSerializer(
            RecipeIngredient.objects.filter(recipe_id=obj.id), many=True
        ).data


class RecipeWriteSerializer(BaseRecipeSerializer):
    """Сериализатор рецептов(запись)."""

    ingredients = RecipeIngredientWriteSerializer(many=True)

    def __fill_fields(self, instance, tags, ingredients):
        instance.tags.add(*[elem.id for elem in tags])
        igredient_through = instance.ingredients.through
        ingredients_list = [
            igredient_through(
                recipe_id=instance.id,
                ingredient_id=ingredient["id"].id,
                amount=ingredient["amount"],
            )
            for ingredient in ingredients
        ]

        igredient_through.objects.bulk_create(ingredients_list)

        instance.save()

    def create(self, validated_data):

        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")

        recipe = Recipe(**validated_data)
        recipe.save()
        self.__fill_fields(recipe, tags, ingredients)
        return recipe

    def update(self, instance, validated_data):

        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")

        instance.name = validated_data["name"]
        instance.text = validated_data["text"]
        instance.cooking_time = validated_data["cooking_time"]

        if "image" in validated_data:
            instance.image = validated_data["image"]

        instance.tags.clear()
        instance.ingredients.clear()

        self.__fill_fields(instance, tags, ingredients)

        return instance

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
            "is_in_shopping_cart",
            "is_favorited",
        )
        read_only_fields = ("author",)


class ShoppingCardSerializer(serializers.ModelSerializer):
    """Сериализатор корзины."""

    user = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = ShoppingCard
        fields = "__all__"
        read_only_fields = ("user", "recipe")


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериазатор избранного."""

    user = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Favorite
        fields = ("user", "recipe")
        read_only_fields = ("user", "recipe")
