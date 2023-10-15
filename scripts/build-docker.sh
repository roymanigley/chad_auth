#!/bin/bash
rm -rf docker/chad_auth/app && \
mkdir docker/chad_auth/app && \
cp chad_auth docker/chad_auth/app -r && \
cp chad_auth_api docker/chad_auth/app -r && \
cp chad_auth_oidc docker/chad_auth/app -r && \
cp templates docker/chad_auth/app -r && \
cp requirements.txt docker/chad_auth/app && \
cp scripts/build-prod.sh docker/chad_auth/app && \
cp scripts/run-prod.sh docker/chad_auth/app && \
cp manage.py docker/chad_auth/app && \
docker-compose -f docker/docker-compose.yml build