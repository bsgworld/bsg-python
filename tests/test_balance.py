#!/usr/bin/env python3

import bsg_restapi as api

# noinspection PyPackageRequirements
from tests.settings import API_KEY

requester = api.BalanceAPI(config=dict(api_key=API_KEY))

BALANCE_ATTRIBUTES = ['amount', 'currency', 'limit']


def test_api_balance_balance_api():
    response = requester.get()
    assert isinstance(response, dict)
    for attribute in BALANCE_ATTRIBUTES:
        assert response.get(attribute)
