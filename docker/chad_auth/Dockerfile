FROM python:3.9.15-slim-bullseye
WORKDIR /opt/app
COPY app /opt/app
RUN /opt/app/build-prod.sh
CMD /opt/app/run-prod.sh