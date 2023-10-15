#!/bin/bash
export DJANGO_SUPERUSER_USERNAME='admin'
export DJANGO_SUPERUSER_PASSWORD='admin'
export DJANGO_SUPERUSER_EMAIL='admin@admin.local'
export CHAD_AUTH_APP_PROFILE='PROD'
python3 -m venv .env && \
source .env/bin/activate && \
pip install -r requirements.txt && \
echo yes | ./manage.py collectstatic && \
./manage.py migrate && \
./manage.py migrate --run-syncdb && \
./manage.py createsuperuser --noinput
