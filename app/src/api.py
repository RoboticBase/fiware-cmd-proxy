# -*- coding: utf-8 -*-
import copy
import os
import json
from logging import getLogger

import requests

from src import const


logger = getLogger(__name__)

def send_request_to_orion(endpoint, value):
    headers = dict()
    headers['Fiware-Service'] = os.environ.get(const.FIWARE_SERVICE, '')
    headers['Fiware-Servicepath'] = os.environ.get(const.FIWARE_SERVICEPATH, '')
    headers['Content-Type'] = 'application/json'

    data = copy.deepcopy(const.ORION_PAYLOAD_TEMPLATE)
    data['contextElements'][0]['id'] = os.environ.get(const.ROBOT_ID, '')
    data['contextElements'][0]['type'] = os.environ.get(const.ROBOT_TYPE, '')
    data['contextElements'][0]['attributes'][0]['value'] = value
    requests.post(endpoint, headers=headers, data=json.dumps(data))
