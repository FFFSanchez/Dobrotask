# Dobro Tasks API Service
Продвинутый трекер задач. Авторизация по токену через djoser. Задачи имеют приоритеты. Можно фильтровать по приоритетам. На задачи можно назначать исполнителя. К задачам можно создавать подзадачи. Есть эндпоинты для получения различных статистических данных по задачам.

Сервис задеплоен на серевер Yandex Cloud, CI/CD настроен через GitHub Workflows, написаны базовые тесты, используется gunicorn, nginx, docker compose, PostgreSQL.

При успешном завершении actions workflow приходит оповещение в телеграм бот.

Подключен мониторинг UptimeRobot, получен https сертификат.

#### Адрес: https://bigbobs.bounceme.net/
### Стек
+ Django DRF
+ PostgreSQL
+ Docker compose
+ Gunicorn
+ Nginx
+ WSL
+ GitHub Workflows CI/CD
+ Yandex Cloud
+ UptimeRobot Monitoring
+ HTTPS Cert
+ Postman

## По проблемам и вопросам запуска писать на https://t.me/lordsanchez
### Как запустить проект:

Клонировать репозиторий:

```
git clone https://github.com/FFFSanchez/Dobrotask.git
```

Добавить свой файл .env в главную папку dobrotask, в ту же, где Dockerfile (SECRET_KEY можно сгенерить тут https://djecrety.ir/):

```
SECRET_KEY=******

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres

DB_HOST=pgdb
DB_PORT=5432

```

Запуск через docker compose:

```
находясь в одной папке с docker-compose.yml

docker compose -f docker-compose.yml up --build -d
docker compose -f docker-compose.yml exec backend python manage.py makemigrations
docker compose -f docker-compose.yml exec backend python manage.py migrate
docker compose -f docker-compose.yml exec backend python manage.py collectstatic
docker compose -f docker-compose.yml exec backend cp -r /app/collected_static/. /app/static_refs_backend/static/

# создать суперюзера если нужен доступ в админку.
docker compose -f docker-compose.yml exec backend python manage.py createsuperuser
```

Готово, сервис запущен и доступен на http://localhost:8000/

Админ панель также настроена и доступна по адресу http://localhost:8000/admin/

# Документация:
Перейти по одной из ссылок:
* http://127.0.0.1:8000/redoc/
* http://127.0.0.1:8000/swagger/


## Примеры запросов к API:
### POSTMAN коллекция: https://www.postman.com/lunar-satellite-489414/workspace/dd/collection/24311673-8c2ef3cc-5c24-4d8b-817f-fd0c89fb1ebd?action=share&creator=24311673
1) Регистрация нового пользователя:
* Отправить POST-запрос http://127.0.0.1:8000/api/auth/users/. В теле запроса указать: 
```
{
    "username": "fff3",
    "email": "fff3@fff.ru",
    "password": "qw2f2f21f3"
}
```

2) Получение токена:
* Отправить POST-запрос http://127.0.0.1:8000/api/auth/token/login/. В теле запроса указать:
```
{
    "username": "fff3",
    "email": "fff3@fff.ru",
    "password": "qw2f2f21f3"
}
```
* В ответ придёт токен в форме:

```
{
    "token": "string"
}
```
3) Авторизация:
* Для авторизации в заголовке запросов нужно указывать токен в формате:
```
Token *token*
```

4) Получение своего профиля пользователя:
* Отправить GET-запрос http://127.0.0.1:8000/api/auth/users/me/.
* Ответ придёт в форме:
```
{
    "id": 1,
    "username": "fff",
    "email": "fff@fff.ru",
    "is_admin": true
}
```
5) Получение всех существующих задач:
* Отправить Get-запрос http://127.0.0.1:8000/api/tasks/. В теле запроса указать:
* В ответе придет список задач. Если у задачи есть подзадачи они будут указаны списком в поле subtasks в компактном формате.
* Любую задачу можно посмотреть в полном формате Get-запросом на http://127.0.0.1:8000/api/tasks/<id задачи>/
* На задачу можно назначить исполнителя Patch-запросом на http://127.0.0.1:8000/api/tasks/<id задачи>/ с указанием в теле запроса:
```
{
    "performer": "username пользователя"
}
```
* По умолчанию исполнителем назначается автор задачи
* Также доступны остальные методы для изменения/удаления задачи. (удалять может только автор, изменять - автор или исполнитель)

6) Получение списка всех задач, на которые пользователь назначен исполнителем:

* Отправить GET-запрос http://127.0.0.1:8000/api/tasks/my_tasks_to_do/.
* Ответ придёт в форме списка задач

7) Получение списка всех задач, у которых пользователь является автором:

* Отправить GET-запрос http://127.0.0.1:8000/api/tasks/my_tasks_created_by_me/.
* Ответ придёт в форме списка задач

8) Получение статистики по задачам пользователя:

* Отправить GET-запрос http://127.0.0.1:8000/api/tasks/my_tasks_statistics/.
* Ответ придёт в форме списка параметров.

9) Получение статистики по категориям задач:

* Отправить GET-запрос http://127.0.0.1:8000/api/tasks/category_statistics/.
* Ответ придёт в форме списка параметров.

10) Добавить подзадачу к задаче:

* Отправить POST-запрос http://127.0.0.1:8000/api/tasks/<task_id>/add_subtask/.
* В запросе все тоже самое, что и при создании обычной задачи, можно указать приоритет и категорию
```
{
    "title": "subtask55",
    "description": "subdesc55",
    "priority": "mid",
    "performer": "username"
    "category": "cat1"
}
```

11) Завершить задачу:

* Отправить пустой POST-запрос http://127.0.0.1:8000/api/tasks/<task_id>/complete_task/.

11) Создать категорию:

* Отправить POST-запрос http://127.0.0.1:8000/api/categories/.

```
{
    "name": "string"
}
```
* Так же доступны остальные методы для оперирования категориями GET, PATCH, DELETE

12) Увидеть задачи отфильтрованные по приоритету:

* Отправить GET-запрос http://127.0.0.1:8000/api/tasks/my_tasks_to_do/?priority=mid. (например mid)
* В ответе будет список задач с таким приоритетом

13) Увидеть задачи отсортированные по приоритету:

* Отправить GET-запрос http://127.0.0.1:8000/api/tasks/my_tasks_to_do/?ordering=priority.
* В ответе будет список задач отсортированные по приоритету - high > mid > low


### Автор: 
Александр Трифонов
