from django.forms import ModelForm
from django.forms.widgets import TextInput
from recipes.models import Tag


class TagForm(ModelForm):
    """
    Форма выбора цвета в админке
    https://django.fun/ru/docs/django/4.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.form
    """
    class Meta:
        model = Tag
        fields = ('name', 'color', 'slug')
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }
