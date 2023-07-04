import re

from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

COLOR_HEX_RE = re.compile("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
color_hex_validator = RegexValidator(
    COLOR_HEX_RE,
    _("Enter a valid hex color, eg. #000000"),
    "invalid",
)

# нашел в django-colorfield, подойдет также если будет hexe
# или вообще создать свое поле  ColorField в котором уже будут
# и валидаторы и остальные плюшки
# https://github.com/fabiocaccamo/django-colorfield/blob/main/colorfield/validators.py