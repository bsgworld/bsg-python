#!/usr/bin/env python3

import datetime
import re
import json
from typing import Union
from uuid import uuid4

import requests


class APIError(Exception):
    def __init__(self, code: Union[str, int] = 'unknown', error_description: str = 'unknown'):
        self.code = code
        self.description = error_description
        super().__init__(
            'Error occurred during request processing. Error code: \'{}\', error reason: \'{}\''.format(
                self.code,
                self.description
            ))


DATETIME_SHORT_RE = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
DATETIME_FULL_RE = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}')


class Response(dict):
    def __init__(self, *args, **kwargs):
        if not kwargs and args and len(args) == 1:
            kwargs = args[0]
        for key, value in kwargs.items():
            if isinstance(value, str):
                if DATETIME_SHORT_RE.match(value):
                    kwargs.update({key: datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')})
                elif DATETIME_FULL_RE.match(value):
                    value = value[:-3] + value[-2:]
                    kwargs.update({key: datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S%z')})
        super(Response, self).__init__(**kwargs)


class Price(Response):
    pass


class Recipient(dict):
    def __init__(self, msisdn: Union[int, str] = None, reference: str = None, **kwargs):
        """
        :type msisdn: str or int, but len(str(msisdn)) <= 15
        """
        if not msisdn or not len(str(msisdn)) <= 15:
            # raise error without real API request, for error codes see https://bsg.world/developers/rest-api/errors/
            raise APIError(code=41, error_description='Invalid MSISDN')
        if not reference:
            reference = uuid4().hex[:8]
        kwargs.update(dict(msisdn=msisdn, reference=reference))
        super().__init__(**kwargs)


class Requester:
    """Base class for any kind of API reqiests"""
    session = requests.Session()

    def __init__(self, config: dict = None):
        """Constructor for Requester"""
        self.config = {'api_endpoint': config.get('api_endpoint', 'https://app.bsg.hk/rest'),
                       'api_key': config.get('api_key')}
        self.headers = {}

    def proceed(self,
                module_name: str,
                function_name: Union[str, int],
                function_param=None,
                method: str = 'GET',
                data: Union[dict, list] = None
                ) -> dict:

        if not self.config['api_endpoint']:
            raise APIError(code=7, error_description='Missing parameters (\'api_endpoint\')')
        url_parts = [self.config['api_endpoint'], module_name, function_name]
        if function_param:
            url_parts.append(str(function_param))
        url = '/'.join(url_parts)

        if not self.config['api_key']:
            raise APIError(code=1, error_description='Invalid API key')
        self.headers.update({'X-API-KEY': self.config['api_key'],
                             'Content-type': 'application/json; charset=utf-8',
                             'Accept': 'application/json ', })
        response = None  # type: requests.Response
        if method == 'GET':
            response = self.session.get(url, verify=True, headers=self.headers, params=data)
        elif method == 'POST':
            response = self.session.post(url, verify=True, headers=self.headers, data=json.dumps(data))
        if not response.ok:
            raise APIError(code=response.status_code, error_description=response.reason if response.reason else 'HTTP error')
        result = response.json()
        if result.get('error'):
            result['error'] = int(result['error'])
            if result['error']:
                raise APIError(code=result['error'], error_description=result.get('errorDescription'))
        return result
