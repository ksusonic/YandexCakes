# Yandex Cakes

##### REST API for online cakes shop on Python 3.9

Версия на фреймворке FastAPI.
В планах переход на Aiohttp.

## Инструкция по применению

### - Запуск на вашем сервере

Сконфигурируйте вашу базу данных 
(поддержка PostgreSQL, SQLite, MySQL, MariaDB)

И измените строку подключения в api/config.py
```SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432/cakes'```

Virtualenv:
```shell
python3 -m venv venv
source venv/bin/activate
```

Установите зависимости:
```shell
pip3 install -r requirements.txt
```

Простой вариант запуска сервера через uvicorn:
```shell
uvicorn api.main:app --reload --host 0.0.0.0 --port 8080
```
Также, можно указать количество воркеров (их кол-во равно кол-ву ядер вашего процессора)
При 4-х ядрах:
```shell
uvicorn api.main:app --reload --workers 4 --host 0.0.0.0 --port 8080
```


