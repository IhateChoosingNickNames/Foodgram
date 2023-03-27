from django.contrib import admin
from django.db.models import Count

from .models import Ingredient, Recipe, RecipeIngredient, Tag


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "measurement_unit")
    search_fields = ("name",)
    list_editable = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
    search_fields = ("name",)
    list_editable = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 2
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    list_display = (
        "pk",
        "name",
        "pub_date",
        "author",
        "tag_list",
        "ingredient_list",
        "favorited_times",
    )

    search_fields = ("name", "author__username", "tags__name")
    list_editable = ("name",)
    filter_horizontal = ("tags",)
    inlines = (RecipeIngredientInline,)

    def favorited_times(self, obj):
        return obj.favorited_times

    def tag_list(self, obj):
        return " | ".join([tag.name for tag in obj.tags.all()])

    def ingredient_list(self, obj):
        return " | ".join(
            [ingredient.name for ingredient in obj.ingredients.all()]
        )

    def get_queryset(self, request):
        return (
            Recipe.objects.select_related("author")
            .prefetch_related("tags", "ingredients")
            .annotate(favorited_times=Count("favorite_object"))
        )
