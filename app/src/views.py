# -*- coding: utf-8 -*-
import os
import json
from logging import getLogger

from flask import request, jsonify, render_template, redirect, url_for
from flask.views import MethodView

from src.api import send_request_to_orion

logger = getLogger(__name__)


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
