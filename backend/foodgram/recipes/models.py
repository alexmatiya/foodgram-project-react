from django.db import models


# Create your models here.
class Tag(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=200,
        unique=True,
        # null=False
    )
    color = models.CharField(
        verbose_name="Цвет в HEX",
        max_length=7,
        unique=True
    )
    # ^[-a-zA-Z0-9_]+$ внутри SlugField
    slug = models.SlugField(
        verbose_name="Уникальный слаг",
        max_length=200,
        unique=True
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name