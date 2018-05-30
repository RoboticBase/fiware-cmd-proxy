#!/bin/sh
sed -i -e "s/<<PORT>>/${PORT}/g" /etc/nginx/conf.d/flask-nginx.conf
/usr/bin/supervisord --nodaemon --configuration /etc/supervisord.conf
