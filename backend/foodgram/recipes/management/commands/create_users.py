from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Создает 7 случайных пользователей'

    def handle(self, *args, **kwargs):
        for i in range(8):
            username = str(i) + "username"
            User.objects.create_user(
                username=username,
                email=f'email@{username}.com',
                password='1234567890',
                first_name=f'first_name_{username}',
                last_name=f'last_name_{username}')

        # User.objects.create_user(
        #     username='newadmin',
        #     email='email@newadmin.com',
        #     password='1234567890',
        #     first_name='first_name_newadmin',
        #     last_name='last_name_newadmin',
        #     is_staff=True,
        #     is_superuser=True)
