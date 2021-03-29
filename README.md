# Yandex Cakes

##### REST API for online cakes shop on Python 3.9

### Версия на фреймворке FastAPI.
В планах:
- написание тестов
- переход на Aiohttp
- асинхронная работа с БД (пока psycopg2)
- Переменные для конфигурации из виртуального окружения
- Подсчет рейтинга для курьеров _(не успел сделать, простите`¯\_(ツ)_/`)_
 
## Архитектура

### 1. Фреймворки и модули:
### [FastAPI](https://github.com/tiangolo/fastapi) ![FastAPI](https://camo.githubusercontent.com/86d9ca3437f5034da052cf0fd398299292aab0e4479b58c20f2fc37dd8ccbe05/68747470733a2f2f666173746170692e7469616e676f6c6f2e636f6d2f696d672f6c6f676f2d6d617267696e2f6c6f676f2d7465616c2e706e67) 

Легкий, производительный и удобный фреймворк для разработки Api. 
Имеет значимые зависимости: **Pydantic** - удобная валидация входных данных, и Starlette - ASGI фреймфорк (для http ответов)


### [SQLAlchemy](https://www.sqlalchemy.org/) ![SQLAlchemy](https://www.sqlalchemy.org/img/sqla_logo.png)
Работа с моделями для хранения в базе данных, с возможностью использовать разные субд.

### 2. База данных
### [PostgreSQL](https://www.postgresql.org/) ![PostgreSQL](https://www.postgresql.org/media/img/about/press/elephant.png) 
На сервере (http://178.154.196.122:8080/) используется PostgreSQL с отдельным пользователем без прав root. Возможно использование другой субд при изменении строки подключения в файле конфигурации `api/config.py`

### 3. Сервер и его конфигурация
### [Ubuntu 20.04.2 LTS](https://ubuntu.com/) ![Ubuntu](https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Logo-ubuntu_cof-orange-hex.svg/231px-Logo-ubuntu_cof-orange-hex.svg.png) 
Выделенный сервер Яндексом на статическом ip `http://178.154.196.122:8080/`
Возможен переход на доменное имя и tls сертификаты при дальнейшем одобрении его хозяев :)
#### На сервере установлен Python 3.9 из бинарников, bash заменен на zsh и oh_my_zsh, подключение возможно как через ssh (и пароль и ключ), так и через mosh (улучшенный ssh)

### Nginx (reverse proxy)
![Nginx](https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Nginx_logo.svg/1024px-Nginx_logo.svg.png)
Реверс-прокси с 127.0.0.1:8000 на публичный 0.0.0.0:8080 для работы Gunicorn
### Gunicorn 
![Gunicorn](https://gunicorn.org/images/logo.jpg) 

WSGI HTTP Server for UNIX


### Как это работает на сервере:

Весь исходный код хранится в `/var/www/yandexcakes`

Запуск и управление происходит через созданный системный сервис `yandexcakes.service`, который запускает Gunicorn с проектом в
`/etc/systemd/system/yandexcakes.service`:
```shell
/var/www/yandexcakes/venv/bin/gunicorn -w 2 -k uvicorn.workers.UvicornWorker api.main:app
```
Это обеспечивает удобную работу с процессом и встроенное логирование в journalctl в Linux/UNIX

## Деплой на локальном сервере

Сконфигурируйте вашу базу данных 
(поддержка PostgreSQL, SQLite, MySQL, MariaDB)

И измените строку подключения в api/config.py
```SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432/cakes'```

Создайте virtualenv:
```shell
python3 -m venv venv
source venv/bin/activate
```

Установите зависимости:
```shell
pip3 install -r requirements.txt
```

Запустите сервера через uvicorn (доступен при установке соответствующей зависимости):
```shell
uvicorn api.main:app --reload --host 0.0.0.0 --port 8080
```
Также, можно указать количество воркеров для улучшения производительности асинхронных операций (их кол-во равно кол-ву ядер вашего процессора)
При 4-х ядрах:
```shell
uvicorn api.main:app --reload --workers 4 --host 0.0.0.0 --port 8080
```
Готово! Переходите на выбранный вами адрес и порт


### Ну все, это конец! Приятных сладостей :3