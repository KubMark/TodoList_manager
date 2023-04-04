# Проект TODOList

[//]: # (## Дипломный проект)

Проект использует следующие технологии:

- Python 3.10
- Django
- PostgreSQL

## Установка

## 1. Создаем виртуальное окружение.

```sh
# для первичной установки
poetry install
# активация окружения
poetry shell
```
## 2. Создайте свой .env файл в корне проекта.

## 3. Заполните .env файл следующими значениями
```sh
SECRET_KEY='your_secret_key'
DEBUG=TrueDB_ENGINE=django.db.backends.engine
DB_NAME=todolist
DB_USER=todolist
DB_PASSWORD=todolist
DB_HOST=localhost
DB_PORT=5432
```
## 4. Создать миграции.
```sh
./manage.py makemigrations
```
## 5. Применить миграции.
```sh
./manage.py migrate
```
## 5. Запустить проект.
```sh
./manage.py runserver
```