#!/usr/bin/env python3

# pylint: disable=import-error
import pytest

import bsg_restapi as api


@pytest.fixture
def requester():
    # noinspection PyPackageRequirements
    from tests.settings import API_KEY
    return api.ViberAPI(config=dict(api_key=API_KEY))


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
    assert exception_info.value.code == 44  # '44': Invalid request payload


def test_message():
    message = api.ViberMessage(text='test message text')
    assert len(message) == 2

    attributes = ['to', 'text']
    for attribute in attributes:
        assert message.get(attribute) is not None

    assert type(message['to']) is list


# noinspection PyShadowingNames
def test_message_add(requester):
    message_from_obj = api.ViberMessage(text='test message text')
    message_from_dict = {'text': 'test message text 1'}

    requester.clear_messages()
    assert not requester.messages

    requester.add_message(message_from_obj)
    requester.add_message(message_from_dict)

    for message in requester.messages:

        assert len(message) == 2

        attributes = ['to', 'text']
        for attribute in attributes:
            assert message.get(attribute) is not None

        assert type(message['to']) is list

    with pytest.raises(api.APIError) as exception_info:
        # noinspection PyTypeChecker
        requester.add_message([])
    assert exception_info.value.code == 45  # '45': Invalid message
    assert hasattr(exception_info.value, 'description')


def test_add_recipient():
    message = api.ViberMessage(text='test message text')

    assert len(message) == 2

    message.add_recipient({'msisdn': '380445556677'})
    message.add_recipient(380445556678)
    message.add_recipient(api.Recipient(380445556679))

    attributes = ['msisdn', 'reference']
    for recipient in message['to']:
        for attribute in attributes:
            assert recipient.get(attribute) is not None


RESPOND_ATTRIBUTES = ['error', 'errorDescription', 'id', 'reference', 'currency', 'price']


# noinspection PyShadowingNames
def test_send_one(requester):
    message = api.ViberMessage(text='test message text to one recipient', to=[api.Recipient(380960000000)])
    respond = requester.send(message=message, sender='BSG')
    for attribute in RESPOND_ATTRIBUTES:
        assert respond['result'][0].get(attribute) is not None


# noinspection PyShadowingNames
def test_send_mul(requester):
    message = api.ViberMessage(text='test message text to many recipients',
                               to=[api.Recipient(380960000001), api.Recipient(380960000002)])

    requester.clear_messages()
    assert not requester.messages

    requester.add_message(message)
    responds = requester.send()
    for respond in responds['result']:
        for attribute in RESPOND_ATTRIBUTES:
            assert respond.get(attribute) is not None


# noinspection PyShadowingNames
def test_get_status(requester):
    message = api.ViberMessage(text='test message text to many recipients',
                               to=[api.Recipient(380960000001), api.Recipient(380960000002)])

    requester.clear_messages()
    assert not requester.messages

    requester.add_message(message)
    response = requester.send()

    status_by_id = requester.get_status(response['result'][0]['id'])
    assert status_by_id
    status_by_ref = requester.get_status(response['result'][0]['reference'])
    assert status_by_ref

    # noinspection PyTypeChecker
    status_by_list = requester.get_status(list())
    assert not status_by_list


# noinspection PyShadowingNames
def test_alt_route(requester):
    requester.clear_messages()
    message = api.ViberMessage(text='test message text to many recipients',
                               to=[api.Recipient(380960000001), api.Recipient(380960000002)],
                               alt_route={'originator': 'BSG',
                                          'text': 'SMS message will be received if you not a VIBER user.'})
    requester.add_message(message)
    responds = requester.send()
    for respond in responds['result']:
        for attribute in RESPOND_ATTRIBUTES:
            assert respond.get(attribute) is not None
