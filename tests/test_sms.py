#!/usr/bin/env python3

# pylint: disable=import-error
import pytest

import bsg_restapi as api


@pytest.fixture
def requester():
    # noinspection PyPackageRequirements
    from tests.settings import API_KEY
    return api.SMSAPI(config=dict(api_key=API_KEY))


# noinspection PyShadowingNames
def test_prices(requester):
    respond_price_list = requester.get_prices()

    assert isinstance(respond_price_list, list)

    assert respond_price_list  # assertion if empty list

    attributes = ['country', 'country_name', 'currency', 'mcc', 'price', 'type']
    for price in respond_price_list:
        for attribute in attributes:
            assert price.get(attribute) is not None


# noinspection PyShadowingNames
def test_send(requester):
    with pytest.raises(api.APIError) as exception_info:
        requester.send()
    assert exception_info.value.code == 26  # '26': Invalid sms text


def test_message():
    message = api.SMSMessage(body='test message text')

    assert len(message) == 2

    attributes = ['body', 'originator']
    for attribute in attributes:
        assert message.get(attribute) is not None

RESPOND_ATTRIBUTES = ['error', 'errorDescription', 'id', 'reference', 'currency', 'price']


# noinspection PyShadowingNames
def test_send_one(requester):
    respond = requester.send(message=api.SMSMessage(body='test message text'), recipients=api.Recipient(380967770002))
    assert respond.get('result')
    for attribute in RESPOND_ATTRIBUTES:
        assert respond['result'].get(attribute) is not None


# noinspection PyShadowingNames
def test_send_mul(requester):
    responds = requester.send(message=api.SMSMessage(body='test message text'), recipients=[api.Recipient(380967770000), api.Recipient(380967770001)])
    assert responds.get('result')
    for respond in responds['result']:
        for attribute in RESPOND_ATTRIBUTES:
            assert respond.get(attribute) is not None


# noinspection PyShadowingNames
def test_get_status_one(requester):
    response = requester.send(message=api.SMSMessage(body='test message text'), recipients=api.Recipient(380967770002))
    assert response.get('result')
    assert response['result'].get('id') is not None
    response['status'] = requester.get_status(response['result']['id'])
    assert response.get('status') is not None


# noinspection PyShadowingNames
def test_get_status_from_internal_message(requester):
    requester.message = api.SMSMessage(body='test message text')
    response = requester.send(recipients=api.Recipient(380967770002))
    assert response.get('result')
    assert response['result'].get('id')
    response['status'] = requester.get_status()
    assert response.get('status') is not None and response.get('status')


# noinspection PyShadowingNames
def test_get_status_from_internal_message_without_send(requester):
    requester.message = api.SMSMessage(body='test message text')
    requester.clear_recipients()
    requester.add_recipient(api.Recipient(380967770003))
    response = requester.get_status()
    assert requester.message.get('status') is not None and response


# noinspection PyShadowingNames
def test_get_status_by_task_id(requester):
    requester.message = api.SMSMessage(body='test message text')
    requester.clear_recipients()
    requester.add_recipient(api.Recipient(380967770004))
    requester.add_recipient(api.Recipient(380967770005))
    response_send = requester.send()
    assert response_send
    response_status = requester.get_status()
    assert requester.message.get('status') is not None and response_status


# noinspection PyShadowingNames
def test_get_status_by_task_id_of_int_message(requester):
    requester.message = api.SMSMessage(body='test message text')
    requester.clear_recipients()
    requester.add_recipient(api.Recipient(380967770006))
    requester.add_recipient(api.Recipient(380967770007))
    response_send = requester.send()
    assert response_send
    response_status = requester.get_status_by_task_id()
    assert requester.message.get('status') is not None and response_status
