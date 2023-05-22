from django.contrib import admin
from django.contrib.admin import display, register

from recipes.models import (Favorite, Ingredient, Recipe, Recipe_ingredient,
                            Shopping_cart, Tag)


@register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')
    empty_value_display = 'Данных нет'


@register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_filter = ('name', )
    search_fields = ('name', )


@register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'ingredients_recipes', 'cooking_time',
                    'text', 'tags_recipes', 'image', 'author', 'in_favorites')
    list_editable = ('name', 'cooking_time', 'text', 'image', 'author')
    readonly_fields = ('in_favorites',)
    list_filter = ('name', 'author', 'tags')
    empty_value_display = 'Данных нет'

    @display(description='Ингредиенты рецепта')
    def ingredients_recipes(self, recipe):
        return [ingredient.name for ingredient in recipe.ingredients.all()]

    @display(description='Теги рецепта')
    def tags_recipes(self, recipe):
        return [tag.name for tag in recipe.tags.all()]

    @display(description='В избранном')
    def in_favorites(self, obj):
        return obj.favorite_recipe.count()


@register(Recipe_ingredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    list_editable = ('recipe', 'ingredient', 'amount')


@register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_editable = ('user', 'recipe')


@register(Shopping_cart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_editable = ('user', 'recipe')
