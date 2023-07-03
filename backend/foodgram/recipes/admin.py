from django.contrib import admin
from recipes.models import (Favorite,  Ingredient, Recipe,
                            RecipeIngredient, ShoppingCart,  Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color',)
    search_fields = ('name', 'color')
    save_on_top = True


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """
    Модель ингредиентов:
    В список вывести название ингредиента и единицы измерения.
    Добавить фильтр по названию.
    """
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)  # фильтровать по такому полю не самая лучая идея


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Модель рецептов:
    В списке рецептов вывести название и автора рецепта.
    Добавить фильтры по автору, названию рецепта, тегам.
    На странице рецепта вывести общее число добавлений этого рецепта
    в избранное.
    """
    list_display = ('pk', 'name', 'author', 'favorites_count')
    list_filter = ('author', 'name', 'tags')
    inlines = (RecipeIngredientInline,)

    def favorites_count(self, obj):
        return obj.favorites.count()


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')
