FROM python:latest

MAINTAINER Alexander van Zyl <vanzyl.alex@gmail.com>

RUN apt-get update \
    && apt-get install -y build-essential sqlite3 \
    && pip install --upgrade pip \
    && pip install Flask \
                   flask_sqlalchemy \
                   flask_restful \
                   marshmallow \
    && apt-get autoclean \
    && apt-get clean

RUN mkdir -p /usr/src/api \
    && chown -R 1000:1000 /usr/src/api

WORKDIR /usr/src/api

EXPOSE 5000

CMD ["python", "api.py"]