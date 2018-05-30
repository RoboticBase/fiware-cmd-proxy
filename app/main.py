#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import logging.config
from logging import getLogger

from flask import Flask, make_response, jsonify

from src.views import GamepadAPI, WebAPI

DEFAULT_PORT = 3000


try:
    with open("logging.json", "r") as f:
        logging.config.dictConfig(json.load(f))
        if ('LOG_LEVEL' in os.environ and
                os.environ['LOG_LEVEL'].upper() in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']):
            for handler in getLogger().handlers:
                if handler.get_name() == 'console':
                    handler.setLevel(getattr(logging, os.environ['LOG_LEVEL'].upper()))
except FileNotFoundError:
    pass


try:
    port = int(os.environ.get('PORT', str(DEFAULT_PORT)))
    if port < 1 or 65535 < port:
        port = DEFAULT_PORT
except ValueError:
    port = DEFAULT_PORT


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
    app.run(host="0.0.0.0", port=port)
