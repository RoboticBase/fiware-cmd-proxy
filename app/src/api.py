# -*- coding: utf-8 -*-
import copy
import os
import json
from urllib.parse import urljoin
from logging import getLogger

from flask import request, jsonify, render_template, redirect, url_for
from flask.views import MethodView

import requests

logger = getLogger(__name__)

ORION_PATH = '/v1/updateContext'
ORION_HEADER = {
    'Fiware-Service': 'demo1',
    'Fiware-Servicepath': '/',
    'Content-Type': 'application/json',
}
ORION_PAYLOAD_TEMPLATE = {
    'contextElements': [
        {
            'id': 'turtlesim',
            'isPattern': False,
            'type': 'demo1',
            'attributes': [
                {
                    'name': 'move',
                    'type': 'string',
                    'value': '',
                }
            ],
        }
    ],
    'updateAction': 'UPDATE',
}

if 'ORION_ENDPOINT' in os.environ:
    ENDPOINT = urljoin(os.environ['ORION_ENDPOINT'], ORION_PATH)
else:
    ENDPOINT = urljoin('http://orion:1026', ORION_PATH)


class GamepadAPI(MethodView):
    NAME = 'gamepad'

    def post(self):
        payload = request.data.decode('utf-8')
        logger.info(f'request payload={payload}')

        for data in json.loads(payload)['data']:
            value = data['button']['value'].strip()
            if len(value) != 0:
                data = copy.deepcopy(ORION_PAYLOAD_TEMPLATE)
                data['contextElements'][0]['attributes'][0]['value'] = value
                requests.post(ENDPOINT, headers=ORION_HEADER, data=json.dumps(data))

        return jsonify({'result': 'ok'})


class WebAPI(MethodView):
    NAME = 'web'

    def get(self):
        return render_template('controller.html')

    def post(self):
        if 'move' in request.form:
            value = request.form['move'].strip()
            if len(value) != 0:
                data = copy.deepcopy(ORION_PAYLOAD_TEMPLATE)
                data['contextElements'][0]['attributes'][0]['value'] = value
                requests.post(ENDPOINT, headers=ORION_HEADER, data=json.dumps(data))

        if 'PREFIX' in os.environ:
            redirect_url = os.path.join('/', os.environ['PREFIX'], *url_for(WebAPI.NAME).split(os.sep)[1:])
        else:
            redirect_url = url_for(WebAPI.NAME)

        return redirect(redirect_url)
