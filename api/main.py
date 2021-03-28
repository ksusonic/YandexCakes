from uvicorn import run
from fastapi import FastAPI

from api.config import desc

app = FastAPI(title="YandexCakes", description=desc)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080)
