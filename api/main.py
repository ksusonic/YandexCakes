from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi import FastAPI

from api.config import desc
from api.handlers import ROUTERS
from db.base import init_db

app = FastAPI(title="YandexCakes", description=desc, docs_url="/")
init_db()

for router in ROUTERS:
    app.include_router(router)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(exc.errors(), status_code=status.HTTP_400_BAD_REQUEST)
