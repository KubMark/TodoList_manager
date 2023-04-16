# Проект TODOList

## Дипломный проект представляет собой Backend-часть для сайта планирования задач.

Проект использует следующие технологии:

- Python 3.10
- Django
- PostgreSQL
- Gunicorn
- Nginx
- Docker

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
SECRET_KEY="todolist"
DEBUG=True
POSTGRES_USER=todolist
POSTGRES_PASSWORD=todolist
POSTGRES_DB=todolist
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