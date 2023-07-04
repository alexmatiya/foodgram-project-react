from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from users.models import User


class Command(BaseCommand):
    help = 'Создает 15 случайных пользователей, 1 суперюзера'

    def handle(self, *args, **kwargs):
        for _ in range(16):
            username = get_random_string(7)
            User.objects.create_user(
                username=username,
                email=f'email@{username}.com',
                password='1234567890',
                first_name=f'first_name_{username}',
                last_name=f'last_name_{username}')

        User.objects.create_user(
            username='newadmin',
            email='email@newadmin.com',
            password='1234567890',
            first_name='first_name_newadmin',
            last_name='last_name_newadmin',
            is_staff=True,
            is_superuser=True)
