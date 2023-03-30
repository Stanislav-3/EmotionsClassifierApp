FROM python:3.11-slim-buster

WORKDIR /usr/src/django_app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIPENV_VENV_IN_PROJECT=1


COPY ./django-app .
COPY .env ../.

#RUN pip install --upgrade pip
RUN pip install -r requirements.txt