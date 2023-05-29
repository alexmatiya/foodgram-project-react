from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    username = models.CharField(
        verbose_name="Уникальный юзернейм",
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=150,
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=150,
        blank=False,
        null=False
    )
    password = models.CharField(
        verbose_name="Пароль",
        max_length=150,
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
