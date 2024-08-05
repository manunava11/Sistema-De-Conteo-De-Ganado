#!/bin/sh
set -e

python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input
chmod 777 /import_model.py
python3 /import_model.py
gunicorn webapp.wsgi:application --bind 0.0.0.0:8000