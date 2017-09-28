FROM node:latest

MAINTAINER Alexander van Zyl <vanzyl.alex@gmail.com>

RUN npm install --global vue-cli

RUN apt-get install -y git \
    && apt-get autoclean \
    && apt-get clean

WORKDIR /var/www/html

CMD ["node"]