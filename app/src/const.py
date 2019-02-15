# -*- coding: utf-8 -*-

# logging
LOGGING_JSON = 'logging.json'
TARGET_HANDLERS = ['console', ]

# flask config
CONFIG_CFG = 'config.cfg'
DEFAULT_ORION_ENDPOINT = 'DEFAULT_ORION_ENDPOINT'
DEFAULT_PORT = 'DEFAULT_PORT'

# environment variable name
LOG_LEVEL = 'LOG_LEVEL'
LISTEN_PORT = 'LISTEN_PORT'
FIWARE_SERVICE = 'FIWARE_SERVICE'
FIWARE_SERVICEPATH = 'FIWARE_SERVICEPATH'
ROBOT_ID = 'ROBOT_ID'
ROBOT_TYPE = 'ROBOT_TYPE'
ORION_ENDPOINT = 'ORION_ENDPOINT'
PREFIX = 'PREFIX'

# orion specification
ORION_PATH = '/v2/entities/<<ROBOT_ID>>/attrs?type=<<ROBOT_TYPE>>'
ORION_PAYLOAD_TEMPLATE = {
    'move': {
        'value': '<<SEND_VALUE>>'
    }
}
