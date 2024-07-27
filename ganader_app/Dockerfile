FROM python:3.11.1-slim-bullseye

ENV PYTHONBUFFERED=1

COPY ./requirements.txt /requirements.txt

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    postgresql-client \
    gcc \
    libpq-dev \
    gfortran \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && pip3 install --upgrade pip \
    && pip3 install -r /requirements.txt \
    && apt-get remove -y gcc gfortran build-essential \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./webapp /app

WORKDIR /app

COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]