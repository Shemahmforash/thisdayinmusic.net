FROM python:3.6

ENV PYTHONUNBUFFERED 1

COPY . /code/
COPY ./thisdayinmusic/.env.example /code/thisdayinmusic/.env

WORKDIR /code/

RUN pip install pipenv
RUN pipenv install --system

EXPOSE 8000
