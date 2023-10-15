#!/bin/bash
export CHAD_AUTH_APP_PROFILE='PROD'
source .env/bin/activate && \
gunicorn chad_auth.wsgi:application --bind 0.0.0.0:8000
