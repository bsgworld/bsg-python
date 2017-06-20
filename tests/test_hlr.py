#!/usr/bin/env python3

# pylint: disable=import-error
import pytest

import bsg_restapi as api


@pytest.fixture
def requester():
    # noinspection PyPackageRequirements
    from tests.settings import API_KEY
    return api.HLRAPI(config=dict(api_key=API_KEY))


# noinspection PyShadowingNames
@pytest.fixture
def sender_mul(requester):
    hlrls = [api.HLRL(msisdn=380960000000), api.HLRL(msisdn=380960000001)]
    return requester, requester.send(hlrls)


AMOUNT = 15


# noinspection PyShadowingNames
@pytest.fixture
def sender_mul_by_internal(requester):
    beg_msisdn = 380960000000
    for msisdn in range(beg_msisdn, beg_msisdn + AMOUNT):
        requester.add_hlrl(msisdn)
    requester.send()
    return requester


# noinspection PyShadowingNames
def test_prices(requester):
    response_price_list = requester.get_prices()

    assert isinstance(response_price_list, list)

    assert response_price_list  # assertion if empty list

    attributes = ['country', 'country_name', 'currency', 'mcc', 'price', 'type']
    for price in response_price_list:
        for attribute in attributes:
            assert price.get(attribute)


# noinspection PyShadowingNames
def test_send(requester):
    with pytest.raises(api.APIError) as exception_info:
        requester.send()
    assert exception_info.value.code == 64  # '64': Invalid request payload


# noinspection PyShadowingNames
def test_add_and_clear(sender_mul_by_internal):
    assert len(sender_mul_by_internal.hlrls) == AMOUNT
    assert isinstance(sender_mul_by_internal.hlrls, list)

    sender_mul_by_internal.clear_hlrls()
    assert not sender_mul_by_internal.hlrls


def test_hlrl():
    hlrl = api.HLRL(msisdn=380960000000)

    assert len(hlrl) == 2

    attributes = ['msisdn', 'reference']
    for attribute in attributes:
        assert hlrl.get(attribute)

RESPOND_ATTRIBUTES = ['error', 'id', 'reference', 'callback_url', 'msisdn', 'tariff_code', 'currency', 'price']


# noinspection PyShadowingNames
def test_send_mul(requester):
    hlrls = [api.HLRL(msisdn=380960000000), api.HLRL(msisdn=380960000001)]
    response = requester.send(hlrls)
    assert response.get('result')
    assert len(response.get('result')) == 2
    for response_ in response['result']:
        for attribute in RESPOND_ATTRIBUTES:
            # need to check for None, else false-positive assertion on error==0
            assert response_.get(attribute) is not None


STATUS_ATTRIBUTES = ['brand', 'createdDatetime', 'error', 'errorDescription', 'id', 'msisdn', 'name', 'name_en', 'name_ru', 'network', 'reference', 'status', 'statusDatetime']
DETAILS_ATTRIBUTES = ['imsi', 'location_msc', 'ported', 'roaming']


# noinspection PyShadowingNames
def test_getstatus(sender_mul):
    requester, response = sender_mul
    respond_ref, respond_id = (response['result'][0]['reference'], response['result'][0]['id'])
    status_by_id = requester.get_status(respond_id)
    status_by_ref = requester.get_status(respond_ref)
    for status in [status_by_id, status_by_ref]:
        assert status is not None
        for attribute in STATUS_ATTRIBUTES:
            assert status.get(attribute) is not None
        if status.get('details'):
            for attribute in DETAILS_ATTRIBUTES:
                assert status['details'].get(attribute) is not None


# noinspection PyShadowingNames
def test_getstatus_for_obj(requester):
    hlrl = api.HLRL(msisdn=380960000000)
    hlrl['result'] = requester.send(hlrl)
    status = requester.get_status(hlrl)
    for attribute in STATUS_ATTRIBUTES:
        assert status.get(attribute) is not None


# noinspection PyShadowingNames
def test_getstatus_for_obj_without_result(requester):
    hlrl = api.HLRL(msisdn=380960000000)
    status = requester.get_status(hlrl)
    for attribute in STATUS_ATTRIBUTES:
        assert status.get(attribute) is not None


# noinspection PyShadowingNames
def test_getstatus_for_internal_hlrls(sender_mul_by_internal):
    sender_mul_by_internal.get_status()
    for hlrl in sender_mul_by_internal.hlrls:
        assert hlrl.get('status')
        for attribute in STATUS_ATTRIBUTES:
            assert hlrl['status'].get(attribute) is not None


# noinspection PyShadowingNames
def test_getstatus_for_internal_hlrls_partly(sender_mul_by_internal):
    sender_mul_by_internal.get_status()
    sender_mul_by_internal.hlrls[-5] = api.HLRL(msisdn=380960000000)
    sender_mul_by_internal.get_status()
    for hlrl in sender_mul_by_internal.hlrls:
        assert hlrl.get('status')
        for attribute in STATUS_ATTRIBUTES:
            assert hlrl['status'].get(attribute) is not None
