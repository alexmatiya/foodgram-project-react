from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Переопределена модель Пользователя.
    Переопределены USERNAME_FIEL, REQUIRED_FIELDS
    из AbstractUser
    """
    email = models.EmailField(
        max_length=254,
        null=False,
        unique=True,
        verbose_name="Адрес электронной почты",
    )
    # username = models.CharField(
    #     blank=False,
    #     max_length=150,
    #     null=False,
    #     unique=True,
    #     verbose_name="Уникальный юзернейм",
    # )
    # first_name = models.CharField(
    #     blank=False,
    #     max_length=150,
    #     null=False,
    #     verbose_name="Имя",
    # )
    # last_name = models.CharField(
    #     blank=False,
    #     max_length=150,
    #     null=False,
    #     verbose_name="Фамилия",
    # )
    # password = models.CharField(
    #     blank=False,
    #     max_length=150,
    #     null=False,
    #     verbose_name="Пароль",
    # )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """
    Модель Подписка. Юзеры подписываются друг на друга.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    def __str__(self):
        return f'Пользователь {self.user.username} \
            подписан на {self.author.username}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
