# -*- coding: utf-8 -*-
import os
import json
from logging import getLogger
from urllib.parse import urljoin

from flask import request, jsonify, render_template, redirect, url_for, current_app
from flask.views import MethodView

from src.api import send_request_to_orion

logger = getLogger(__name__)

ORION_PATH = '/v1/updateContext'


class OrionEndpointMixin:
    ORION_ENDPOINT = None

    @classmethod
    def get_orion_endpoint(cls):
        if cls.ORION_ENDPOINT is None:
            if 'ORION_ENDPOINT' in os.environ:
                cls.ORION_ENDPOINT = urljoin(os.environ['ORION_ENDPOINT'], ORION_PATH)
            else:
                cls.ORION_ENDPOINT = urljoin(current_app.config['DEFAULT_ORION_ENDPOINT'], ORION_PATH)
        return cls.ORION_ENDPOINT


class GamepadAPI(OrionEndpointMixin, MethodView):
    NAME = 'gamepad'

    def post(self):
        payload = request.data.decode('utf-8')
        logger.info(f'request payload={payload}')

        for data in json.loads(payload)['data']:
            value = data['button']['value'].strip()
            if len(value) != 0:
                send_request_to_orion(GamepadAPI.get_orion_endpoint(), value)

        return jsonify({'result': 'ok'})


class WebAPI(OrionEndpointMixin, MethodView):
    NAME = 'web'

    def get(self):
        return render_template('controller.html')

    def post(self):
        if 'move' in request.form:
            value = request.form['move'].strip()
            if len(value) != 0:
                send_request_to_orion(WebAPI.get_orion_endpoint(), value)

        if 'PREFIX' in os.environ:
            redirect_url = os.path.join('/', os.environ['PREFIX'], *url_for(WebAPI.NAME).split(os.sep)[1:])
        else:
            redirect_url = url_for(WebAPI.NAME)

        return redirect(redirect_url)
