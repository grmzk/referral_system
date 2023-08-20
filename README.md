# **Referral System API**
Реализует простую реферальную систему.

[Полная документация в формате ReDoc](http://93.115.19.207/redoc/)

##### Технологии
- Python 3.10
- Django 4.2
- Django REST Framework 3.14.0
- Gunicorn 20.2
- PostgreSQL 15
- Nginx 1.24
- Docker

##### Как запустить проект:

Клонировать репозиторий и перейти в директорию `infra` в командной строке:

```
git clone git@github.com:grmzk/referral_system.git
```

```
cd referral_system/infra/
```

Для работы с другой СУБД отредактировать `.env`

```
DB_ENGINE=django.db.backends.postgresql # СУБД 
DB_NAME=postgres                        # название БД
POSTGRES_USER=postgres                  # имя пользователя БД
POSTGRES_PASSWORD=postgres              # пароль пользователя БД
DB_HOST=db                              # адрес хоста с БД
DB_PORT=5432                            # порт для подключения к БД
```

Собрать контейнер и запустить Referral System:

```
docker-compose up -d
```


Выполнить (только после первой сборки):

```
docker-compose exec referral_system python manage.py migrate
```

##### Эндпоинты

Получить список всех пользователей:
```
GET /api/users/
```

Профиль конкретного пользователя по username (телефонный номер):
```
GET /api/users/{username}/
```

[Полный список эндпоинтов](http://93.115.19.207/redoc/)

##### Авторы
- Игорь Музыка [mailto:igor@mail.fake]
