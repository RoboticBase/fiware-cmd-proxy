# -*- coding: utf-8 -*-
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

    data = json.dumps(const.ORION_PAYLOAD_TEMPLATE)
    data = data.replace('<<ROBOT_ID>>', os.environ.get(const.ROBOT_ID, '')) \
               .replace('<<ROBOT_TYPE>>', os.environ.get(const.ROBOT_TYPE, '')) \
               .replace('<<SEND_VALUE>>', value if value is not None else '<<null>>') \
               .replace('"<<null>>"', 'null')
    requests.post(endpoint, headers=headers, data=data)
