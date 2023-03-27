import re

from djoser.serializers import UserSerializer as DefaultUserSerializer
from recipes.models import Recipe
from rest_framework import serializers

from users.models import Subscription, User


class UserRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class CustomUserSerializer(DefaultUserSerializer):
    """Кастомный сериализатор пользователей."""

    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        if self.context["request"].user.is_authenticated:
            if hasattr(obj, "is_subscribed"):
                return obj.is_subscribed
            return Subscription.objects.filter(
                user=self.context["request"].user, author=obj
            ).exists()
        return False

    def get_recipes(self, obj):
        recipe_count = 3
        path = self.context["request"].get_full_path()
        recipe_limit = re.search(r"recipes_limit=(\d+)", path)

        if recipe_limit:
            recipe_count = int(recipe_limit.group(1))

        return UserRecipeSerializer(
            Recipe.objects.filter(author=obj)[:recipe_count], many=True
        ).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор подписки/отписки."""

    user = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Subscription
        fields = ("user", "author")
        read_only_fields = ("author", "user")


class SubscriptionListSerializer(serializers.ModelSerializer):
    """Сериализатор списка подписок."""

    author = CustomUserSerializer()

    class Meta:
        model = Subscription
        fields = ("author",)
        read_only_fields = ("user",)
