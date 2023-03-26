import re

from core.models import AbstractModel
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Recipe(AbstractModel):
    """Модель рецептов."""

    image = models.ImageField(_("Картинка"), upload_to="photos/%Y/%m/%d")
    text = models.TextField(_("Текстовое описание"), max_length=500)
    ingredients = models.ManyToManyField(
        "Ingredient",
        verbose_name=_("Ингредиенты"),
        related_name="recipes",
        through="RecipeIngredient",
    )
    tags = models.ManyToManyField(
        "Tag", verbose_name=_("Тэг"), related_name="recipes"
    )
    author = models.ForeignKey(
        User,
        verbose_name=_("Автор"),
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    cooking_time = models.PositiveIntegerField(
        _("Время приготовления"), validators=[MinValueValidator(1)]
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = _("Рецепт")
        verbose_name_plural = _("Рецепты")
        constraints = (
            models.UniqueConstraint(
                fields=("name", "author"),
                name="unique name + author",
            ),
        )

    def __str__(self):
        return self.name[:50]


class Ingredient(AbstractModel):
    """Модель ингредиентов."""

    measurement_unit = models.CharField(_("Единицы измерения"), max_length=50)

    class Meta:
        ordering = ("name",)
        verbose_name = _("Ингредиент")
        verbose_name_plural = _("Ингредиенты")
        constraints = (
            models.UniqueConstraint(
                fields=("name", "measurement_unit"),
                name="unique name + measurement_unit",
            ),
        )

    def __str__(self):
        return self.name[:50]


class RecipeIngredient(models.Model):
    """Промежуточная таблица для М:М рецептов и ингредиентов."""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name=_("Рецепт"),
        on_delete=models.CASCADE,
        related_name="recipe_ingr",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name=_("Ингредиент"),
        on_delete=models.CASCADE,
        related_name="ingr_recipe",
    )
    amount = models.PositiveIntegerField(
        _("Общее доступное количество"), validators=[MinValueValidator(1)]
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=("recipe", "ingredient"),
                name="unique recipe + ingredient",
            ),
        )


class Tag(AbstractModel):
    """Модель тэгов."""

    color = models.CharField(
        _("Цветовой HEX-код"),
        max_length=7,
        unique=True,
        validators=(
            RegexValidator(
                re.compile("^#[A-Fa-f0-9]{6}$"),
                _("Введите валидный цветовой HEX-код в формате <#AAAAAA>"),
                "invalid",
            ),
        ),
    )
    slug = models.SlugField(
        _("Слаг"), auto_created=True, max_length=128, unique=True
    )

    class Meta:
        ordering = ("name",)
        verbose_name = _("Тэг")
        verbose_name_plural = _("Тэги")

    def __str__(self):
        return self.name[:50]


class ShoppingCard(models.Model):
    """Модель продуктовой корзины."""

    user = models.ForeignKey(
        User,
        verbose_name=_("Владелец списка"),
        on_delete=models.CASCADE,
        related_name="shopping_card",
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name=_("Рецепт"),
        on_delete=models.CASCADE,
        related_name="shopping_card",
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=("user", "recipe"),
                name="unique recipe in shopping card",
            ),
        )


class Favorite(models.Model):
    """Модель избранного."""

    user = models.ForeignKey(
        User,
        verbose_name=_("Текущий пользователь"),
        related_name="favorite",
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name=_("Какой рецепт добавить в избранное"),
        related_name="favorite_object",
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=("user", "recipe"), name="unique favorite"
            ),
        )
