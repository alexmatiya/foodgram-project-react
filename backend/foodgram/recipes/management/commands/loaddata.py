# https://tretyakov.net/post/kak-sozdavat-polzovatelskie-komandy-upravleniya-django/
# https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/
# https://stackoverflow.com/questions/2459979/how-to-import-csv-data-into-django-models
import csv

from django.core.management import BaseCommand
from recipes.models import Ingredient


MODELS_FIELDS = {}


class Command(BaseCommand):
    help = 'Загрузка данных из csv файлов'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            help="путь к файлу"
        )

    def handle(self, *args, **options):
        file_path = options['path']
        with open(file_path) as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                _, _ = Ingredient.objects.get_or_create(
                    name=row[0].capitalize(),
                    measurement_unit=row[1],
                )
