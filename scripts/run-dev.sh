#!/bin/bash
export CHAD_AUTH_APP_PROFILE='DEV'
source .env/bin/activate && \
./manage.py runserver
