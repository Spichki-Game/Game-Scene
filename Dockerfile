FROM python:3.11-slim


MAINTAINER SciBourne <bourne-sci-hack@yandex.ru>

LABEL Description="Game Scene microservice" \
    Vendor="Samael Arts <SciBourne>" \
    Version="0.1.0"


ENV TZ=Europe/Moscow

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


WORKDIR /srv/Game-Scene
RUN useradd game-scene

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install lsb-release
RUN apt-get -y install git

RUN apt-get -y install redis
RUN service redis-server start


COPY src src
COPY pyproject.toml ./
COPY README.md ./
COPY LICENSE ./

RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install

RUN chown -hR game-scene /srv/Game-Scene
USER game-scene:game-scene

EXPOSE 50051/tcp
CMD poetry run server
