# -*- coding: utf-8 -*-

# logging
LOGGING_JSON = 'logging.json'
TARGET_HANDLERS = ['console', ]

# flask config
CONFIG_CFG = 'config.cfg'
DEFAULT_ORION_ENDPOINT = 'DEFAULT_ORION_ENDPOINT'

# environment variable name
LOG_LEVEL = 'LOG_LEVEL'
DEFAULT_PORT = 'DEFAULT_PORT'
FIWARE_SERVICE = 'FIWARE_SERVICE'
FIWARE_SERVICEPATH = 'FIWARE_SERVICEPATH'
ROBOT_ID = 'ROBOT_ID'
ROBOT_TYPE = 'ROBOT_TYPE'
ORION_ENDPOINT = 'ORION_ENDPOINT'
PREFIX = 'PREFIX'

# orion specification
ORION_PATH = '/v1/updateContext'
ORION_PAYLOAD_TEMPLATE = {
    'contextElements': [
        {
            'id': '<<ROBOT_ID>>',
            'isPattern': False,
            'type': '<<ROBOT_TYPE>>',
            'attributes': [
                {
                    'name': 'move',
                    'type': 'string',
                    'value': '<<SEND_VALUE>>',
                }
            ],
        }
    ],
    'updateAction': 'UPDATE',
}
