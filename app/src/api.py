# -*- coding: utf-8 -*-
import copy
import os
import json
from logging import getLogger

import requests

logger = getLogger(__name__)

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


def send_request_to_orion(endpoint, value):
    headers = dict()
    headers['Fiware-Service'] = os.environ.get('FIWARE_SERVICE', 'demo1')
    headers['Fiware-Servicepath'] = os.environ.get('FIWARE_SERVICEPATH', '/')
    headers['Content-Type'] = 'application/json'

    data = copy.deepcopy(ORION_PAYLOAD_TEMPLATE)
    data['contextElements'][0]['id'] = os.environ.get('ROBOT_ID', '')
    data['contextElements'][0]['type'] = os.environ.get('ROBOT_TYPE', '')
    data['contextElements'][0]['attributes'][0]['value'] = value
    requests.post(endpoint, headers=headers, data=json.dumps(data))
