from django.core.validators import MinValueValidator
from django.db import transaction
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.utils import create_ingredients
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import Subscription, User


class RecipeShortSerializer(serializers.ModelSerializer):
    """
    Сериализатор для работы с краткой информацией о рецепте.
    """
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class UserSignUpSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователя."""
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class UserGetSerializer(UserSerializer):
    """Сериализатор для профиля пользователя."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and Subscription.objects.filter(
                user=request.user, author=obj
            ).exists()
        )


class UserSubscribeRepresentSerializer(UserGetSerializer):
    """"
    Сериализатор вывода авторов на которых подписан текущий пользователь.
    """
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        read_only_fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        recipes = obj.recipes.all()
        if recipes_limit:
            recipes = obj.recipes.all()[:int(recipes_limit)]
        return RecipeShortSerializer(
            recipes, many=True,
            context={'request': request}
        ).data

    def get_recipes_count(self, obj):
        """Kоличество рецептов у каждого автора."""
        return obj.recipes.count()


class UserSubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки/отписки от пользователей."""
    class Meta:
        model = Subscription
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'author'),
                message='Вы уже подписаны на этого пользователя')
        ]

    def validate(self, data):
        request = self.context.get('request')
        if request.user == data['author']:
            raise serializers.ValidationError(
                'Нельзя подписываться на самого себя!'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        return UserSubscribeRepresentSerializer(
            instance.author, context={'request': request}
        ).data


class TagSerialiser(serializers.ModelSerializer):
    """
    Сериализатор для Тегов
    """
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода ингридиентов.
    """
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class IngredientGetSerializerInRecipe(serializers.ModelSerializer):
    """Сериализатор для получения информации об ингредиентах в рецептах.
    """
    id = serializers.IntegerField(source='ingredient.id', read_only=True)
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class IngredientPostSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления ингредиентов.
    Используется при работе с рецептами.
    """
    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        validators=(
            MinValueValidator(
                1,
                message='Количество ингредиента должно быть 1 или более.'
            ),
        )
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'amount'
        )


class RecipeGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации о рецепте.
    https://pypi.org/project/drf-extra-fields/
    """
    tags = TagSerialiser(many=True, read_only=True)
    author = UserGetSerializer(read_only=True)
    ingredients = IngredientGetSerializerInRecipe(
        many=True,
        read_only=True,
        source='recipeingredients'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=False)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and Favorite.objects.filter(
                user=request.user, recipe=obj
            ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and ShoppingCart.objects.filter(
                user=request.user, recipe=obj
            ).exists()
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для добаления/обновления рецепта."""
    ingredients = IngredientPostSerializer(
        source='recipeingredients',
        many=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    def validate(self, data):
        """
        Проверка ингредиентов.
        """
        ingredients_list = []
        ingredients = data
        for ingredient in ingredients.get('recipeingredients'):
            ingredients_list.append(ingredient.get('id'))
        if len(set(ingredients_list)) != len(ingredients_list):
            raise serializers.ValidationError(
                'Вы пытаетесь добавить в рецепт два одинаковых ингредиента'
            )
        return data

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('recipeingredients')
        tags = validated_data.pop('tags')
        request = self.context.get('request')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)
        create_ingredients(ingredients, recipe)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('recipeingredients')
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        RecipeIngredient.objects.filter(recipe=instance).delete()
        super().update(instance, validated_data)
        create_ingredients(ingredients, instance)
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeGetSerializer(
            instance,
            context={'request': request}
        ).data


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с избранными рецептами."""

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже добавлен в избранное')
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeShortSerializer(instance.recipe, context=context).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для работы со списком покупок."""
    class Meta:
        model = ShoppingCart
        fields = (
            'user',
            'recipe'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже добавлен в список покупок')
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeShortSerializer(
            instance.recipe,
            context={'request': request}
        ).data
