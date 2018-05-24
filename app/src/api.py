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
ORION_PAYLOAD_TEMPLATE = {
    'contextElements': [
        {
            'id': '',
            'isPattern': False,
            'type': '',
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


def send_request_to_orion(value):
    headers = dict()
    headers['Fiware-Service'] = os.environ.get('FIWARE_SERVICE', 'demo1')
    headers['Fiware-Servicepath'] = os.environ.get('FIWARE_SERVICEPATH', '/')
    headers['Content-Type'] = 'application/json'

    data = copy.deepcopy(ORION_PAYLOAD_TEMPLATE)
    data['contextElements'][0]['id'] = os.environ.get('ROBOT_ID', '')
    data['contextElements'][0]['type'] = os.environ.get('ROBOT_TYPE', '')
    data['contextElements'][0]['attributes'][0]['value'] = value
    requests.post(ENDPOINT, headers=headers, data=json.dumps(data))


class GamepadAPI(MethodView):
    NAME = 'gamepad'

    def post(self):
        payload = request.data.decode('utf-8')
        logger.info(f'request payload={payload}')

        for data in json.loads(payload)['data']:
            value = data['button']['value'].strip()
            if len(value) != 0:
                send_request_to_orion(value)

        return jsonify({'result': 'ok'})


class WebAPI(MethodView):
    NAME = 'web'

    def get(self):
        return render_template('controller.html')

    def post(self):
        if 'move' in request.form:
            value = request.form['move'].strip()
            if len(value) != 0:
                send_request_to_orion(value)

        if 'PREFIX' in os.environ:
            redirect_url = os.path.join('/', os.environ['PREFIX'], *url_for(WebAPI.NAME).split(os.sep)[1:])
        else:
            redirect_url = url_for(WebAPI.NAME)

        return redirect(redirect_url)
