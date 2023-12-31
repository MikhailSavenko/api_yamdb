# Описание проекта
Проект предназначен для публикаций произведений, на которые можно оставлять отзывы и добавлять рейтинг, а также комментировать эти отзывы. Пользователи могут регистрироваться на сайте, создавать профиль, добавлять свои произведения и просматривать произведения других пользователей. Кроме того, пользователи могут оставлять отзывы и ставить рейтинги произведениям других пользователей.

# Установка
Для запуска проекта сначала необходимо установить Python 3 и Django. Для установки выполните следующие команды:

```
sudo apt-get update
sudo apt-get install python3
sudo apt-get install python3-pip
pip3 install django
```

После установки Django выполните команду: **pip install pandas.**

# Запуск проекта
Для запуска проекта на локальном сервере выполните следующие команды:

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

# Команды управления Django
Реализованы две пользовательские команды управления Django:

python manage.py dataimport <имя модели> <путь к файлу с данными> - импорт данных из файла .csv в базу данных.
python manage.py dataimportall - заполнение базы данных данными из файлов: users.csv, titles.csv, category.csv, genre.csv, genretitle.csv, review.csv, comments.csv. Данные файла расположены в директории static/data.

# Используемые технологии
- Python 3
- Django
- HTML
- CSS
- JavaScript
- Pandas

# Авторы
Проект разработан командой разработчиков. Контактная информация разработчиков может быть найдена на сайте проекта.