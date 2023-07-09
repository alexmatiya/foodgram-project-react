прогнать миграции:
sudo docker-compose exec web manage.py migrate

sudo docker-compose exec web python manage.py createsuperuser 
sudo docker-compose exec web python manage.py collectstatic --no-input

загрузить ингредиенты:
sudo docker-compose exec web python manage.py loaddata --path recipes/management/commands/ingredients.csv


Создать 15 случайных пользователей, 1 суперюзера:
sudo docker-compose exec web python manage.py create_users