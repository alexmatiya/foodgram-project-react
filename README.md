1. Прогнать миграции:
```
sudo docker-compose exec web manage.py migrate
```
2. Создать суперюзера:
```
sudo docker-compose exec web python manage.py createsuperuser
```
3. Собрать статику:
```
sudo docker-compose exec web python manage.py collectstatic --no-input
```
4. Загрузить ингредиенты:
```
sudo docker-compose exec web python manage.py loaddata --path recipes/management/commands/ingredients.csv
```
----------------------
#### для проверки:
Электронная почта: admin@admin.admin

Пароль: admin

host: http://158.160.50.115/