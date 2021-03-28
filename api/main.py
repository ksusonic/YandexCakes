from uvicorn import run
from fastapi import FastAPI

from api.config import desc
from api.handlers import ROUTERS
from db.base import init_db

app = FastAPI(title="YandexCakes", description=desc)
init_db()

for router in ROUTERS:
    app.include_router(router)

if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080)
