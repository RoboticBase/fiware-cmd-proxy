# -*- coding: utf-8 -*-
import json
import os

import pytest

import requests

from src.orion import send_request_to_orion
from src import const


class TestSendRequestToOrion:

    def teardown_method(self, method):
        if const.FIWARE_SERVICE in os.environ:
            del os.environ[const.FIWARE_SERVICE]
        if const.FIWARE_SERVICEPATH in os.environ:
            del os.environ[const.FIWARE_SERVICEPATH]
        if const.ROBOT_ID in os.environ:
            del os.environ[const.ROBOT_ID]
        if const.ROBOT_TYPE in os.environ:
            del os.environ[const.ROBOT_TYPE]

    @pytest.fixture
    def ep(self):
        return 'http://test.example.com:1026/test/'

    @pytest.mark.parametrize('v', [None, '', ' ', 'test value'])
    def test_success_no_env(self, monkeypatch, ep, v):
        def mocked_post(endpoint, headers, data):
            assert endpoint == ep
            assert isinstance(headers, dict)
            assert headers == {
                'Fiware-Service': '',
                'Fiware-Servicepath': '',
                'Content-Type': 'application/json',
            }
            assert isinstance(data, str)
            assert json.loads(data) == {
                'contextElements': [
                    {
                        'id': '',
                        'isPattern': False,
                        'type': '',
                        'attributes': [
                            {
                                'name': 'move',
                                'type': 'string',
                                'value': v,
                            }
                        ],
                    }
                ],
                'updateAction': 'UPDATE',
            }

        monkeypatch.setattr(requests, 'post', mocked_post)
        send_request_to_orion(ep, v)

    @pytest.mark.parametrize('fs', ['', ' ', 'test service'])
    @pytest.mark.parametrize('fsp', ['', ' ', 'test servicepath'])
    @pytest.mark.parametrize('ri', ['', ' ', 'test robot id'])
    @pytest.mark.parametrize('rt', ['', ' ', 'test robot type'])
    @pytest.mark.parametrize('v', [None, '', ' ', 'test value'])
    def test_success_env(self, monkeypatch, ep, fs, fsp, ri, rt, v):
        os.environ[const.FIWARE_SERVICE] = fs
        os.environ[const.FIWARE_SERVICEPATH] = fsp
        os.environ[const.ROBOT_ID] = ri
        os.environ[const.ROBOT_TYPE] = rt

        def mocked_post(endpoint, headers, data):
            assert endpoint == ep
            assert isinstance(headers, dict)
            assert headers == {
                'Fiware-Service': fs,
                'Fiware-Servicepath': fsp,
                'Content-Type': 'application/json',
            }
            assert isinstance(data, str)
            assert json.loads(data) == {
                'contextElements': [
                    {
                        'id': ri,
                        'isPattern': False,
                        'type': rt,
                        'attributes': [
                            {
                                'name': 'move',
                                'type': 'string',
                                'value': v,
                            }
                        ],
                    }
                ],
                'updateAction': 'UPDATE',
            }

        monkeypatch.setattr(requests, 'post', mocked_post)
        send_request_to_orion(ep, v)

    def test_raise_error(self, monkeypatch, ep):
        def mocked_post(endpoint, headers, data):
            raise requests.exceptions.RequestException()

        monkeypatch.setattr(requests, 'post', mocked_post)
        with pytest.raises(requests.exceptions.RequestException):
            send_request_to_orion(ep, 'dummy')
