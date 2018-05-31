# -*- coding: utf-8 -*-
import json
import os

import pytest

import requests

from src import const


class TestGamepadAPI:

    @pytest.mark.parametrize('v', [None, '', ' ', 'test value', '   test value 2   '])
    def test_success_no_env_2(self, monkeypatch, endpoint, mocked_post, client, v):
        mocked_post(monkeypatch, endpoint, '', '', '', '', v.strip() if v is not None else None)

        data = {
            'data': [
                {
                    'button': {
                        'value': v,
                    },
                },
            ],
        }
        response = client.post('/gamepad/', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'
        if v is not None and len(v.strip()) != 0:
            assert response.json == {'result': 'ok', 'requested': True, 'value': v.strip()}
        else:
            assert response.json == {'result': 'ok', 'requested': False}

    @pytest.mark.parametrize('fs', ['', ' ', 'test service'])
    @pytest.mark.parametrize('fsp', ['', ' ', 'test servicepath'])
    @pytest.mark.parametrize('ri', ['', ' ', 'test robot id'])
    @pytest.mark.parametrize('rt', ['', ' ', 'test robot type'])
    @pytest.mark.parametrize('v', [None, '', ' ', 'test value', '   test value 2   '])
    def test_success_env(self, monkeypatch, endpoint, mocked_post, client, fs, fsp, ri, rt, v):
        os.environ[const.FIWARE_SERVICE] = fs
        os.environ[const.FIWARE_SERVICEPATH] = fsp
        os.environ[const.ROBOT_ID] = ri
        os.environ[const.ROBOT_TYPE] = rt

        mocked_post(monkeypatch, endpoint, fs, fsp, ri, rt, v.strip() if v is not None else None)

        data = {
            'data': [
                {
                    'button': {
                        'value': v,
                    },
                },
            ],
        }
        response = client.post('/gamepad/', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'
        if v is not None and len(v.strip()) != 0:
            assert response.json == {'result': 'ok', 'requested': True, 'value': v.strip()}
        else:
            assert response.json == {'result': 'ok', 'requested': False}

    def test_raise_error(self, monkeypatch, endpoint, client):
        v = 'dummy'

        def mocked_post(endpoint, headers, data):
            raise requests.exceptions.RequestException()

        monkeypatch.setattr(requests, 'post', mocked_post)

        data = {
            'data': [
                {
                    'button': {
                        'value': v,
                    },
                },
            ],
        }
        response = client.post('/gamepad/', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 500
        assert response.headers['Content-Type'] == 'application/json'
        assert response.json == {'error': 'Internal Server Error'}


class TestNotFound:

    def test_not_found(self, monkeypatch, endpoint, mocked_post, client):
        v = 'dummy'

        mocked_post(monkeypatch, endpoint, '', '', '', '', v)

        data = {
            'data': [
                {
                    'button': {
                        'value': v,
                    },
                },
            ],
        }
        response = client.post('/invalid/', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 404
        assert response.headers['Content-Type'] == 'application/json'
        assert response.json == {'error': 'Not Found'}


class TestMethodNotAllowed:

    @pytest.mark.parametrize('method', ['get', 'put', 'patch', 'delete', 'head'])
    def test_method_not_allowed(self, monkeypatch, endpoint, client, method):
        v = 'dummy'

        data = {
            'data': [
                {
                    'button': {
                        'value': v,
                    },
                },
            ],
        }
        response = getattr(client, method)('/gamepad/', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 405
        assert response.headers['Content-Type'] == 'application/json'
        if method != 'head':
            assert response.json == {'error': 'Method Not Allowed'}
