#!/usr/bin/env python3

# pylint: disable=import-error
import pytest

import bsg_restapi as api

# noinspection PyPackageRequirements
from tests.settings import API_KEY


def test_requester():
    response = api.Requester(config=dict(api_key=API_KEY)).proceed('common', 'balance')
    assert isinstance(response, dict)


def test_http_error():
    requester = api.Requester(config=
                              dict(api_key=API_KEY,
                                   api_endpoint='https://bsg.world/test_for_wrong_endpoint'))
    with pytest.raises(api.APIError) as exception_info:
        requester.proceed('common', 'balance' + '_INVALIDATE')
    assert exception_info.value.code == 404  # '404': Not Found


def test_empty_endpoint():
    requester = api.Requester(config=
                              dict(api_key=API_KEY,
                                   api_endpoint=''))
    with pytest.raises(api.APIError) as exception_info:
        requester.proceed('common', 'balance')
    assert exception_info.value.code == 7  # '7': 'Missing parameters ('api_endpoint')'


def test_empty_api_key():
    requester = api.Requester(config=
                              dict(api_key=''))
    with pytest.raises(api.APIError) as exception_info:
        requester.proceed('common', 'balance')
    assert exception_info.value.code == 1  # '1': 'Invalid API key'


def test_invalid_msisdn():
    with pytest.raises(api.APIError) as exception_info:
        api.Recipient('')
    assert exception_info.value.code == 41  # '41': 'Invalid MSISDN'
    assert hasattr(exception_info.value, 'description')
    with pytest.raises(api.APIError) as exception_info:
        api.Recipient('380968890000@')
    assert exception_info.value.code == 41  # '41': 'Invalid MSISDN'


def test_api_error():
    requester = api.Requester(config=dict(api_key=API_KEY + '_INVALIDATE'))
    with pytest.raises(api.APIError) as exception_info:
        requester.proceed('common', 'balance')
    assert exception_info.value.code == 1  # '1': Invalid API key
