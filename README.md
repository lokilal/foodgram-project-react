## foodgram-project-react
### Описание
Продуктовая соц. сеть для любителей рецептов
Проект диплома яндекс практикума

### Проект доступен по ссылке :
http://51.250.104.198/recipes


## Описание Workflow

##### Workflow состоит из четырёх шагов:

1. Проверка кода на соответствие PEP8, запуск тестов проекта.
2. Сборка и публикация образа на DockerHub.
3. Автоматический деплой на выбранный сервер.
4. Отправка ботом уведомления в телеграм-чат.


## Подготовка и запуск проекта
##### Клонирование репозитория
```bash
git clone https://github.com/lokilal/foodgram-project-react.git
```

## Установка на удаленном сервере (Ubuntu):
##### Шаг 1. Вход на удаленный сервер
Подключаемся на удаленный сервер
```bash
ssh <username>@<ip_address>
```

##### Шаг 2. Установка docker:

```bash
sudo apt install docker.io 
```

##### Шаг 3. Установка docker-compose:

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

##### Шаг 4. Копирование docker-compose.yaml и nginx/default.conf:
Скопируйте подготовленные файлы `docker-compose.yaml` и `nginx/default.conf` из проекта на сервер в `home/<ваш_username>/docker-compose.yaml` и `home/<ваш_username>/nginx/default.conf` соответственно.


```bash
scp docker-compose.yaml <username>@<host>:/home/<username>/docker-compose.yaml
scp -r nginx/ <username>@<host>:/home/<username>/
```

##### Шаг 5.  Добавление Github Secrets:
Для работы с Workflow добавьте в Secrets GitHub переменные окружения для работы:
```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

DOCKER_PASSWORD=<pass DockerHub>
DOCKER_USERNAME=<login DockerHub>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<passphrase для сервера, если он установлен>
SSH_KEY=<SSH ключ>

TELEGRAM_TO=<ID своего телеграм-аккаунта. Для инфо @myidbot>
TELEGRAM_TOKEN=<токен бота>
```

##### Шаг 6. После успешного деплоя:
```bash
sudo docker-compose exec web python manage.py migrate 
sudo docker-compose exec web python manage.py collectstatic --no-input
sudo docker-compose exec web python manage.py add_ingredients
```
SSH_KEY=<SSH ключ>

TELEGRAM_TO=<ID своего телеграм-аккаунта. Для инфо @myidbot>
TELEGRAM_TOKEN=<токен бота>
```

##### Шаг 6. После успешного деплоя:
```bash
sudo docker-compose exec web python manage.py migrate 
sudo docker-compose exec web python manage.py collectstatic --no-input
```

[![Django-app workfow](https://github.com/lokilal/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/lokilal/foodgram-project-react/actions/workflows/foodgram_workflow.yml)
