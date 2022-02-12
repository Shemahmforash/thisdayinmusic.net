FROM python:3.10.0b2

ENV PYTHONUNBUFFERED 1

COPY . /code/
COPY ./thisdayinmusic/.env.example /code/thisdayinmusic/.env

WORKDIR /code/

RUN pip install pipenv
RUN pipenv install --system

EXPOSE 8000
