FROM python:3.11-slim-buster

WORKDIR /usr/src/django_app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIPENV_VENV_IN_PROJECT 1

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY django_app/ .
COPY .env ../.

#RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt