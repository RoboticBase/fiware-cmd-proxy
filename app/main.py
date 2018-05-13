#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import logging.config
from logging import getLogger

from flask import Flask, make_response, jsonify

from src.api import GamepadAPI, WebAPI

logger = getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description='cmd-proxy')
    parser.add_argument('-p', '--port', action='store', nargs='?', const=3000, default=3000, type=int, help='listening port')
    return parser.parse_args()


def setup_logging():
    log_level = 'INFO'
    if ('LOG_LEVEL' in os.environ and
            os.environ['LOG_LEVEL'].upper() in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']):
        log_level = os.environ['LOG_LEVEL'].upper()

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s [%(levelname)7s] %(name)s - %(message)s',
                'datefmt': '%Y/%m/%d %H:%M:%S',
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'default',
                'stream': 'ext://sys.stdout',
            }
        },
        'loggers': {
            '': {
                'level': log_level,
                'handlers': ['console'],
            }
        }
    })


setup_logging()
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.add_url_rule('/gamepad/', view_func=GamepadAPI.as_view(GamepadAPI.NAME))
app.add_url_rule('/web/', view_func=WebAPI.as_view(WebAPI.NAME))


@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(500)
def error_handler(error):
    name = error.name if hasattr(error, 'name') else 'Internal Server Error'
    code = error.code if hasattr(error, 'code') else 500
    return make_response(jsonify({'error': name}), code)


if __name__ == '__main__':
    args = parse_args()
    app.run(host="0.0.0.0", port=args.port)
