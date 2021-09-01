# api_yamdb

# Оглавление
1. [Описание проекта](https://github.com/Yakov-Varnaev/api_yamdb/blob/master/README.md#описание-проекта)
     1. [Функционал](https://github.com/Yakov-Varnaev/api_yamdb/blob/master/README.md#функционал)
2. [Запуск проекта](https://github.com/Yakov-Varnaev/api_yamdb/blob/master/README.md#запуск-проекта)
3. [Создание суперпользователя](https://github.com/Yakov-Varnaev/api_yamdb/blob/master/README.md#создание-суперпользователя)
4. [Документация](https://github.com/Yakov-Varnaev/api_yamdb/blob/main/README.md#документация)
     1. [Авторизация внутри swagger](https://github.com/Yakov-Varnaev/api_yamdb/blob/main/README.md#Авторизация-внутри-swagger)
5. [CURL команды](https://github.com/Yakov-Varnaev/api_yamdb/blob/main/README.md#curl-команды)
     1. [Регистрация](https://github.com/Yakov-Varnaev/api_yamdb/blob/main/README.md#регистрация)
     2. [Получения токена](https://github.com/Yakov-Varnaev/api_yamdb/blob/main/README.md#получения-токена)
     3. [Информация о пользователе](https://github.com/Yakov-Varnaev/api_yamdb/blob/main/README.md#информация-о-пользователе)
     4. [Создания поста](https://github.com/Yakov-Varnaev/api_yamdb/blob/main/README.md#создания-поста)
     5. [Создание комментария](https://github.com/Yakov-Varnaev/api_yamdb/blob/main/README.md#создание-комментария)
     6. [Подписка на пользователя](https://github.com/Yakov-Varnaev/api_yamdb/blob/main/README.md#подписка-на-пользователя)
6. [TODO](https://github.com/Yakov-Varnaev/api_yamdb/blob/main/README.md#todo)


# Описание проекта
[Оглавление](https://github.com/Yakov-Varnaev/api_yamdb/blob/main/README.md#оглавление)


## Функционал
[Оглавление](https://github.com/Yakov-Varnaev/api_yamdb/blob/main/README.md#оглавление)


# Запуск проекта
[Оглавление](https://github.com/Yakov-Varnaev/api_yamdb/blob/main/README.md#оглавление)


1. Склонируйте данный репозиторий
```
git clone https://github.com/Yakov-Varnaev/api_yamdb.git
```

2. Перейдите в директорию api_yamdb/
```
cd api_yamdb/
```

3. Создайте и активируйте виртуальное окружение
```
# api_yamdb/
python3 -m venv venv
source venv/bin/activate
```

4. Установите все необходимые модули
```
pip install --upgrade pip
pip install -r requirements.txt
```

5. Выполните миграции
Для этого необходимо перейти в директорию api_yamdb/api_yamdb/.
```
~ cd api_yamdb/
```
Выполните мграции
```
python3 manage.py migrate users
python3 manage.py migrate titles
python3 manage.py migrate reviews
```

6. Запустите сервер

```
python3 manage.py runserver
```
Если все выполнено верно, то вы должны увидеть в консоли следующее:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
August 31, 2021 - 19:17:30
Django version 2.2.6, using settings 'api_yamdb.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

# Создание суперпользователя
[Оглавление](https://github.com/Yakov-Varnaev/api_yamdb/blob/main/README.md#оглавление)

Вам может пригодиться супер-пользователь - он позволяет быстро и удобно создавать пользователей, посты, комментарии и другие сущности.
Для этого вам будет, находясь в директории `secure_blog/secure_blog/`, выполнить следующие команды:
```
python3 manage.py createsuperuser
```
Введите все необходимые поля.
### Обратите внимание, что при вводе паролей, в консоли ничего не отображается, после введения пароля просто нажмите <kbd>Enter</kbd>.

Панель админа будет доступна по ссылке: `localhost:8000/admin/`






