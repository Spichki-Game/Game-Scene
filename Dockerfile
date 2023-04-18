FROM python:3.11-slim


MAINTAINER SciBourne <bourne-sci-hack@yandex.ru>

LABEL Description="Game Scene microservice" \
    Vendor="Samael Arts <SciBourne>" \
    Version="0.1.0"


ENV TZ=Europe/Moscow

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


WORKDIR /srv/Game-Scene

RUN useradd game-scene && \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install lsb-release && \
    apt-get -y install git && \
    apt-get -y install redis

COPY --chown=game-scene:game-scene . ./

RUN pip install poetry && \
    poetry config virtualenvs.in-project true && \
    poetry install


EXPOSE 50051/tcp
ENTRYPOINT ["/srv/Game-Scene/startup-service.sh"]
