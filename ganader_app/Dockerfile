FROM python:3.11.1-alpine3.17

ENV PYTHONBUFFERED=1

RUN apk add --update --no-cache postgresql-client build-base postgresql-dev

COPY ./requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt

COPY ./webapp /app

WORKDIR /app

COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]