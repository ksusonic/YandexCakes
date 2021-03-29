FROM python:3.9

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

EXPOSE 80

COPY ./api /api
COPY ./db /db

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]