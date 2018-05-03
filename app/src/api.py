# -*- coding: utf-8 -*-
import copy
import json
from logging import getLogger

from flask import request, jsonify
from flask.views import MethodView

import requests

logger = getLogger(__name__)

ORION_ENDPOINT = 'http://orion:1026/v1/updateContext'
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


class GamepadAPI(MethodView):
    def post(self):
        payload = request.data.decode('utf-8')
        logger.info(f'request payload={payload}')

        for data in json.loads(payload)['data']:
            value = data['button']['value'].strip()
            if len(value) != 0:
                data = copy.deepcopy(ORION_PAYLOAD_TEMPLATE)
                data['contextElements'][0]['attributes'][0]['value'] = value
                requests.post(ORION_ENDPOINT, headers=ORION_HEADER, data=json.dumps(data))

        return jsonify({'result': 'ok'})
