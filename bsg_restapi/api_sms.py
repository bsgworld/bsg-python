#!/usr/bin/env python3

from typing import Union, List

from .api import Requester, Response, Recipient, Price


class SMSMessage(dict):
    def __init__(self, body: str = '', originator: str = 'BSG RESTAPI', **kwargs):
        kwargs.update({'body': body, 'originator': originator})
        super().__init__(**kwargs)


class SMSAPI(Requester):
    def __init__(self, *args, **kwargs):
        message_params = {'body': kwargs.pop('message_body')} if kwargs.get('message_body') else {}
        message_params.update({'originator': kwargs.pop('message_originator')} if kwargs.get('message_originator') else {})
        self.message = SMSMessage(**message_params)
        self.recipients = []
        super().__init__(*args, **kwargs)

    def get_prices(self, tariff: int = None) -> list:
        result = Response(self.proceed('sms', 'prices', function_param=tariff))
        for index, price in enumerate(result['prices']):
            result['prices'][index] = Price(**price)
        return result['prices']

    def get_status(self, sms_id: Union[str, int] = None) -> dict:
        result = Response(self.proceed('sms', str(sms_id))) if sms_id and isinstance(sms_id, int) else {}
        result = Response(self.proceed('sms', 'reference', sms_id)) if sms_id and isinstance(sms_id, str) else result
        if self.message and not sms_id:
            if not self.message.get('result'):
                self.message['result'] = Response(self.send())
            # at this point we can have or self.message['result']['id'] self.message['result']['task_id']
            if self.message['result'].get('task_id'):
                result = self.get_status_by_task_id(self.message['result']['task_id'])
            else:
                result = Response(self.proceed('sms', str(self.message['result']['result']['id'])))
            self.message['status'] = result
        return result

    def get_status_by_task_id(self, task_id: Union[int, str] = None) -> dict:
        result = Response(self.proceed('sms', 'task', str(task_id))) if task_id else {}
        if self.message and not task_id:
            if self.message.get('result'):
                result = Response(self.proceed('sms', 'task', str(self.message['result']['task_id'])))
                self.message['status'] = result
        return result

    def add_recipient(self, *args, **kwargs):
        self.recipients.append(args[0] if len(args) == 1 and isinstance(args[0], Recipient) else Recipient(*args, **kwargs))

    def clear_recipients(self):
        self.recipients = []

    def send(self,
             message: SMSMessage = None,
             recipients: Union[Recipient, List[Recipient]] = None,
             tariff: int = None,
             validity: int = 72) -> dict:

        data = dict(message if message else self.message)
        if not recipients:
            recipients = self.recipients
        if isinstance(recipients, Recipient):
            data['destination'] = 'phone'
            recipients['msisdn'] = str(recipients['msisdn'])
            data.update(**recipients)
        elif isinstance(recipients, list):
            for recipient in recipients:  # in SMS API smisdn is str
                recipient['msisdn'] = str(recipient['msisdn'])
            data['destination'] = 'phones'
            data['phones'] = recipients
        data.update({'tariff': tariff} if tariff else {})
        data.update({'validity': validity} if validity else {})
        results = Response(self.proceed('sms', 'create', method='POST', data=data))
        if not message:
            self.message['result'] = results
        if isinstance(results['result'], list):
            for result in results['result']:
                if result.get('id'):  # in case of error 'id' key not in results
                    result['id'] = int(result['id'])
        elif isinstance(results['result'], dict):
            if results['result'].get('id'):  # in case of error 'id' key are absent
                results['result']['id'] = int(results['result']['id'])
        return results
