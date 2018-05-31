#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import logging.config
from logging import getLogger

from flask import Flask, make_response, jsonify

from src.views import GamepadAPI, WebAPI
from src import const

try:
    with open(const.LOGGING_JSON, "r") as f:
        logging.config.dictConfig(json.load(f))
        if (const.LOG_LEVEL in os.environ and
                os.environ[const.LOG_LEVEL].upper() in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']):
            for handler in getLogger().handlers:
                if handler.get_name() in const.TARGET_HANDLERS:
                    handler.setLevel(getattr(logging, os.environ[const.LOG_LEVEL].upper()))
except FileNotFoundError:
    pass


app = Flask(__name__)
app.config.from_pyfile(const.CONFIG_CFG)
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
    default_port = app.config[const.DEFAULT_PORT]
    try:
        port = int(os.environ.get('PORT', str(default_port)))
        if port < 1 or 65535 < port:
            port = default_port
    except ValueError:
        port = default_port

    app.run(host="0.0.0.0", port=port)
