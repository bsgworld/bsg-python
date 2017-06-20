#!/usr/bin/env python3

from typing import Union

from .api import Requester, Response, Price, Recipient


class HLRL(Recipient):
    def __init__(self, *args, tariff: int = None, callback_url: str = None, **kwargs):
        kwargs.update({'tariff': tariff} if tariff else {})
        kwargs.update({'callback_url': callback_url} if callback_url else {})
        super().__init__(*args, **kwargs)


class HLRAPI(Requester):
    def __init__(self, *args, **kwargs):
        self.hlrls = []
        super().__init__(*args, **kwargs)

    def get_prices(self, tariff: int = None) -> list:
        result = Response(self.proceed('hlr', 'prices', function_param=tariff))
        for index, price in enumerate(result.get('prices', [])):
            result['prices'][index] = Price(**price)
        return result['prices']

    def get_status(self, hlrl_id: Union[str, int, HLRL] = None) -> Union[dict, list]:
        if hlrl_id:
            if isinstance(hlrl_id, str):
                return Response(self.proceed('hlr', 'reference', hlrl_id))
            elif isinstance(hlrl_id, HLRL):
                if not hlrl_id.get('result'):  # lookup request not previously sended, send it
                    hlrl_id['result'] = self.send(hlrl_id)
                hlrl_id = hlrl_id['result']['result'][0]['id']  # use 'id' from result, now type(hlrl_id) is int
            if isinstance(hlrl_id, int):  # for both of int, HLRL
                return Response(self.proceed('hlr', str(hlrl_id)))
        elif self.hlrls:
            elements_without_result = [el for el in self.hlrls if not el.get('result')]
            if elements_without_result:
                response = self.send(elements_without_result)
                for idx, element in enumerate(elements_without_result):
                    # setting element['result'] and associated self.hlrls['result']
                    element['result'] = response['result'][idx]
            for hlrl in self.hlrls:
                hlrl['status'] = Response(self.proceed('hlr', str(hlrl['result']['id'])))
            return self.hlrls

    def add_hlrl(self, *args, **kwargs):
        self.hlrls.append(args[0] if len(args) == 1 and isinstance(args[0], HLRL) else HLRL(*args, **kwargs))

    def clear_hlrls(self):
        self.hlrls = []

    def send(self, hlrl: Union[HLRL, list] = None) -> dict:
        data = [hlrl] if hlrl and isinstance(hlrl, HLRL) else []
        data = hlrl if hlrl and isinstance(hlrl, list) else data
        data = data if data else self.hlrls
        results = Response(self.proceed('hlr', 'create', method='POST', data=data))
        for index, result in enumerate(results['result']):
            data[index]['result'] = result
            if data[index]['result'].get('id'): # no 'id'  in case of error
                data[index]['result']['id'] = int(data[index]['result']['id'])
        return results
