# Яндекс.Практикум. Спринт 5

#### Папка: hw04_tests
#### Группа: когорта 25
#### Когда: 2021 год
#### Кто: Алексей Ерёменко ( https://github.com/dnHyper/ )

------------

## Вместо вступления:
Если вы проходите обучение по курсу Яндекс.Практикум Python-разработчик, и должны выполнить финальный проект очередного спринта, то … рекомендую подсматривать выложенный мной код лишь *в крайнем случае*. Лично я, во время написания данного кода, использовал лишь подсказки ревьюера, поисковик и документацию по python & django, советую и вам поступать таким же образом.

------------

# Описание:
Продолжение работы над начатой, в третьем спринте, [социальной сетью](https://github.com/dnHyper/hw02_community). В рамках данного спринта было добавлено тестирование ссылок, моделей и форм для:

- Posts
- Users
- About

## Запуск проекта

Создайте и активируйте виртуальное окружение

    python3 -m venv venv
    source venv/bin/activate

Установие зависимости из файла requirements.txt

    python3 -m pip install --upgrade pip
    pip install -r requirements.txt

Выполните миграции

    python3 manage.py migrate


Создайте администратора

    python3 manage.py createsuperuser

Запустите проект

    python3 manage.py runserver

## Возможные проблемы

На данный момент никаких проблем при разворачивании приложения быть не должно. Стоит только учитывать, что база данных создаётся пустой, потому стоит перед началом работы минимально наполнить её, добавив хотя-бы одну группу и пост.

Приложение запускается только на локальном компьютере, категорически советую не выпускать его в сеть. Если хочется получить к нему доступ в рамках домашней локальной сети, требуется настроить роутер, отредактировать настройки, разрешив доступ со всех адресов в **yatube/settings.py (Не безопасно!)**

    ALLOWED_HOSTS = ['*']

Запустите проект

    python3 manage.py runserver 0.0.0.0:8000

## Лицензия
[MIT](https://ru.wikipedia.org/wiki/%D0%9B%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F_MIT)


