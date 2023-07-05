# from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from recipes.models import Ingredient, RecipeIngredient


# def create_ingredients(ingredients, recipe):
#     """Функция для добавления ингредиентов.
#     Используется при создании/редактировании рецепта.
#     Создадим через bulk_create чтобы было меньше запросов к БД.
#     """
#     list_ingredients = []
#     for ingredient in ingredients:
#         cur_ingredient = get_object_or_404(
#             Ingredient,
#             id=ingredient.get('id')
#         )

#         ingredient_amount = ingredient.get('amount')
#         list_ingredients.append(
#             RecipeIngredient(
#                 recipe=recipe,
#                 ingredient=cur_ingredient,
#                 amount=ingredient_amount
#             )
#         )
#     RecipeIngredient.objects.bulk_create(list_ingredients)


# про лишний запрос написал в пачку, возможно таким способом
# смогу немного нагрузку на БД снизить
# все коменту удалю после ревью

def create_ingredients(ingredients, recipe):
    """Функция для добавления ингредиентов.
    Используется при создании/редактировании рецепта.
    Создадим через bulk_create чтобы было меньше запросов к БД.
    """
    list_ingredients = []

    for ingredient in ingredients:
        ingredient_id = ingredient.get('id')

        try:
            cur_ingredient = Ingredient.objects.get(id=ingredient_id)
        except ObjectDoesNotExist:
            continue

        ingredient_amount = ingredient.get('amount')
        list_ingredients.append(
            RecipeIngredient(
                recipe=recipe,
                ingredient=cur_ingredient,
                amount=ingredient_amount
            )
        )

    RecipeIngredient.objects.bulk_create(list_ingredients)
