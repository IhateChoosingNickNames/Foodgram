from django.contrib import admin

from .models import Ingredient, Recipe, Tag


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
    filter_horizontal = ("tags", "ingredients")
