#!/bin/bash
export CHAD_AUTH_APP_PROFILE='DEV'
export DJANGO_SUPERUSER_USERNAME='admin'
export DJANGO_SUPERUSER_PASSWORD='admin'
export DJANGO_SUPERUSER_EMAIL='admin@admin.local'
python3 -m venv .env && \
source .env/bin/activate && \
pip install -r requirements.txt && \
./manage.py migrate && \
./manage.py createsuperuser --noinput
