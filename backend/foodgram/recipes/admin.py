from django.contrib import admin
from django.utils.html import format_html
from recipes.forms import TagForm
from recipes.models import (Favorite,  Ingredient, Recipe,
                            RecipeIngredient, ShoppingCart,  Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    form = TagForm
    list_display = ('name', 'slug', 'color_code',)
    search_fields = ('name', 'color')
    save_on_top = True
    empty_value_display = '-пусто-'

    @admin.display(description='Colored')
    def color_code(self, obj: Tag):
        return format_html(
            '<span style="color: #{};">{}</span>',
            obj.color[1:], obj.color
        )
    color_code.short_description = 'Цветовой код тэга'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 3


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'favorites_amount')
    search_fields = ('name', 'author')
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '-пусто-'
    inlines = [RecipeIngredientInline, ]

    def favorites_amount(self, obj):
        return obj.favorites.count()


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = '-пусто-'
