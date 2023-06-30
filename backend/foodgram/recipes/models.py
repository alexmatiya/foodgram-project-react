from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


# Create your models here.
class Tag(models.Model):
    """
    Тег должен описываться такими полями:
    Название.
    Цветовой HEX-код (например, #49B64E).
    Slug.
    Все поля обязательны для заполнения и уникальны.

    Модель для группировки рецептов по тэгам.
    Связь с Recipe многие ко многим
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название",
        help_text='Название тега',
    )
    color = models.CharField(
        max_length=7,
        verbose_name="Цвет в HEX",
        help_text='Выберите цвет для тега в HEX, например, #49B64E',
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Уникальный слаг",
        help_text='Придумайте уникальный URL адрес для тега',
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Модель для описания ингредиентов.
    Связань с Recipe многие ко многим
    """
    name = models.CharField(
        help_text="Введите название ингредиента",
        max_length=200,
        verbose_name="Название",
        blank=False,
    )
    measurement_unit = models.CharField(
        help_text="Введите единицу измерения",
        max_length=200,
        verbose_name="Единица измерения",
        blank=False,
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Модель для рецептов
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор рецепта",
    )
    cooking_time = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1, 'Значение не может быть меньше 1')],
        verbose_name="Время приготовления в минутах",
    )
    image = models.ImageField(
        verbose_name="Изображение рецепта",
        upload_to="media/",
        blank=True,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты для рецепта',
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Название рецепта",
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
    )
    text = models.TextField(
        max_length=1000,
        verbose_name="Описание рецепта",
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'Рецепет "{self.name}" от {self.author}'


class RecipeIngredient(models.Model):
    """
    Промежуточная таблица между Recipe и Ingredient
    """
    amount = models.IntegerField(
        default=1,
        validators=[MinValueValidator(
            1, 'Количество выбранных ингредиентов не может быть меньше 1')],
        verbose_name="Количество",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="recipeingredients",
        verbose_name="Ингредиент"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipeingredients",
        verbose_name="Рецепт"
    )

    def __str__(self):
        return self.ingredient.name

    class Meta:
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецепте"


class Favorite(models.Model):
    """
    Избранные пользователем рецепты
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Рецепт",
    )

    class Meta:
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_user_recipe_favorite"
            )
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = "Избранные"

    def __str__(self):
        return f'{self.user.username} добавил в избраннное {self.recipe.name}'


class ShoppingCart(models.Model):
    """
    Список покупок. Промежуточная таблица между юзером и рецептом.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="carts",
        verbose_name="Владелец списка покупок"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="carts",
        verbose_name="Рецепт в спике покупок"
    )

    class Meta:
        ordering = ["-id"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_user_recipe_cart"
            )
        ]
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"

    def __str__(self):
        return (f'{self.user.username} добавил'
                f'{self.recipe.name} в список покупок')
