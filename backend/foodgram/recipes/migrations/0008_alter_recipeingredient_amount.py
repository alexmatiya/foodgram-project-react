# Generated by Django 4.2.1 on 2023-07-04 08:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_alter_recipe_cooking_time_alter_tag_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, 'Количество выбранных ингредиентов не может быть меньше 1')], verbose_name='Количество'),
        ),
    ]
