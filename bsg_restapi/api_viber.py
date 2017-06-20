#!/usr/bin/env python3

from typing import Union

from .api import Requester, Response, APIError, Price, Recipient


class ViberMessage(dict):
    def __init__(self, *args, **kwargs):
        kwargs['to'] = kwargs.get('to', [])
        kwargs['text'] = kwargs.get('text', '')
        if kwargs.get('alt_route'):
            kwargs['options'] = dict(viber=dict(alt_route=kwargs.pop('alt_route')))
        super().__init__(*args, **kwargs)

    def add_recipient(self, recipient: Union[dict, int, Recipient] = None):
        recipient_ = recipient if recipient and isinstance(recipient, Recipient) else {}
        recipient_ = Recipient(recipient) if recipient and isinstance(recipient, int) else recipient_
        recipient_ = Recipient(**recipient) if recipient and isinstance(recipient, dict) else recipient_
        self['to'].append(recipient_)


class ViberAPI(Requester):
    def __init__(self, *args, **kwargs):
        self.messages = kwargs.pop('messages', [])
        self.sender = kwargs.pop('sender', 'BSG')
        super(ViberAPI, self).__init__(*args, **kwargs)

    def get_prices(self, tariff: int = None) -> list:
        result = Response(self.proceed('viber', 'prices', function_param=tariff))
        for index, price in enumerate(result['prices']):
            result['prices'][index] = Price(**price)
        return result['prices']

    def get_status(self, message_id: Union[str, int]) -> dict:
        result = {}
        if isinstance(message_id, int):
            result = Response(self.proceed('viber', str(message_id)))
        elif isinstance(message_id, str):
            result = Response(self.proceed('viber', 'reference', message_id))
        return result

    def add_message(self, message: Union[dict, ViberMessage] = None, alpha_name: str = None):
        self.sender = alpha_name if alpha_name else self.sender
        if isinstance(message, ViberMessage):
            self.messages.append(message)
        elif isinstance(message, dict):
            self.messages.append(ViberMessage(**message))
        else:
            raise APIError(code=45, error_description='Invalid message')

    def clear_messages(self):
        self.messages = []

    def send(self,
             message: ViberMessage = None,
             sender: str = None,
             tariff: int = None, validity: int = 86400) -> dict:

        data = {'messages': [message] if message else self.messages}
        sender = sender if sender else self.sender
        for message_ in data['messages']:
            if not message_.get('alpha_name'):
                message_['alpha_name'] = sender
        data.update({'tariff': tariff} if tariff else {})
        data.update({'validity': validity} if validity else {})
        results = self.proceed('viber', 'create', method='POST', data=data)
        for result in results['result']:
            if result.get('id'):
                result['id'] = int(result['id'])
        return results
