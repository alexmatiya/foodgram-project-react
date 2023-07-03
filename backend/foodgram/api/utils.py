from django.shortcuts import get_object_or_404
from recipes.models import Ingredient, RecipeIngredient


def create_ingredients(ingredients, recipe):
    """Функция для добавления ингредиентов.
    Используется при создании/редактировании рецепта.
    Создадим через bulk_create чтобы было меньше запросов к БД.
    """
    list_ingredients = []
    for ingredient in ingredients:
        cur_ingredient = get_object_or_404(Ingredient,
                                           id=ingredient.get('id'))
        infredient_amount = ingredient.get('amount')
        list_ingredients.append(
            RecipeIngredient(
                recipe=recipe,
                ingredient=cur_ingredient,
                amount=infredient_amount)
        )
    RecipeIngredient.objects.bulk_create(list_ingredients)
