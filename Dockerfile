FROM python:3.6.5-alpine
MAINTAINER Nobuyuki Matsui <nobuyuki.matsui@gmail.com>

ARG PORT
ENV PORT ${PORT:-3000}

COPY ./app /opt/fiware-cmd-proxy

WORKDIR /opt/fiware-cmd-proxy

RUN apk update && \
    apk add --no-cache nginx supervisor && \
    apk add --no-cache --virtual .build python3-dev build-base linux-headers pcre-dev && \
    pip install -r requirements/common.txt && \
    pip install -r requirements/production.txt && \
    rm /etc/nginx/nginx.conf && \
    apk del --purge .build && \
    rm -r /root/.cache

COPY nginx.conf /etc/nginx/nginx.conf
COPY flask-nginx.conf /etc/nginx/conf.d/flask-nginx.conf
COPY uwsgi.ini /etc/uwsgi/uwsgi.ini
COPY supervisord.conf /etc/supervisord.conf

RUN sed -i -e "s/<<PORT>>/${PORT}/g" /etc/nginx/conf.d/flask-nginx.conf

EXPOSE $PORT
ENTRYPOINT ["/usr/bin/supervisord", "--nodaemon", "--configuration", "/etc/supervisord.conf"]