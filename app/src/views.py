# -*- coding: utf-8 -*-
import os
import json
from logging import getLogger
from urllib.parse import urljoin

from flask import request, jsonify, render_template, redirect, url_for, current_app
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from src.orion import send_request_to_orion
from src import const

logger = getLogger(__name__)


class OrionEndpointMixin:
    ORION_ENDPOINT = None

    @classmethod
    def get_orion_endpoint(cls):
        if cls.ORION_ENDPOINT is None:
            if const.ORION_ENDPOINT in os.environ:
                cls.ORION_ENDPOINT = urljoin(os.environ[const.ORION_ENDPOINT], const.ORION_PATH)
            else:
                cls.ORION_ENDPOINT = urljoin(current_app.config[const.DEFAULT_ORION_ENDPOINT], const.ORION_PATH)
        return cls.ORION_ENDPOINT


class GamepadAPI(OrionEndpointMixin, MethodView):
    NAME = 'gamepad'

    def post(self):
        data = request.data.decode('utf-8')
        logger.info(f'request data={data}')

        if data is None or len(data.strip()) == 0:
            raise BadRequest()

        payload = json.loads(data)
        if (payload is None or not isinstance(payload, dict) or
                'data' not in payload or not isinstance(payload['data'], list)):
            raise BadRequest()

        result = {'result': 'ok', 'requested': False}

        for data in payload['data']:
            if (isinstance(data, dict) and 'button' in data and
                    isinstance(data['button'], dict) and 'value' in data['button']):
                value = data['button']['value']
                if value is not None and isinstance(value, str) and len(value.strip()) != 0:
                    send_request_to_orion(GamepadAPI.get_orion_endpoint(), value.strip())
                    result['requested'] = True
                    result['value'] = value.strip()

        return jsonify(result)


class WebAPI(OrionEndpointMixin, MethodView):
    NAME = 'web'

    def get(self):
        return render_template('controller.html')

    def post(self):
        if 'move' in request.form:
            value = request.form['move'].strip()
            if len(value) != 0:
                send_request_to_orion(WebAPI.get_orion_endpoint(), value)

        if const.PREFIX in os.environ:
            redirect_url = os.path.join('/',
                                        os.environ.get(const.PREFIX, '').strip(),
                                        *url_for(WebAPI.NAME).split(os.sep)[1:])
        else:
            redirect_url = url_for(WebAPI.NAME)

        return redirect(redirect_url)
