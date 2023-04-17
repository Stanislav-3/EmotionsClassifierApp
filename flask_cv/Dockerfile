FROM python:3.11-slim-buster

WORKDIR /usr/src/flask_cv

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIPENV_VENV_IN_PROJECT 1
ENV KAFKA_BOOTSTRAP_SERVERS kafka:9092

COPY flask_cv/ .
COPY .env ../.

#RUN pip install --upgrade pip
RUN pip install -r requirements.txt