FROM python:3.11.1-alpine3.17

ENV PYTHONBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apk add --update --no-cache postgresql-client build-base postgresql-dev

RUN pip3 install -r requirements.txt

COPY . .

CMD python3 manage.py runserver 0.0.0.0:8000