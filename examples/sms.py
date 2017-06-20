#!/usr/bin/env python3

import sys
import os
import pprint

sys.path.append(os.path.abspath(os.sep.join([os.path.dirname(__file__), '..'])))
import bsg_restapi as api


def main():
    from examples.settings import API_KEY

    try:
        client = api.SMSAPI(config={'api_key': API_KEY})
        prices = client.get_prices()
        print('SMS Prices (first 5 elements from {}): \n{}'.format(len(prices), pprint.pformat(prices[0:5], indent=4)))

        recipient = api.Recipient(380967000000)
        print('Created recipient: \n{}'.format(pprint.pformat(recipient)))
        result = client.send(message=api.SMSMessage('hello from bsg.world'), recipients=recipient)
        print('Current SMS send API result: \n{}'.format(pprint.pformat(result, indent=4)))
        status = client.get_status(result['result']['reference'])
        print('Current SMS status result: \n{}\n'.format(pprint.pformat(status, indent=4)))

        recipient0 = api.Recipient(380967000001)
        recipient1 = api.Recipient(380967000002)
        print('Created another one recipients: \n{}'.format(pprint.pformat([recipient0, recipient1])))
        results = client.send(message=api.SMSMessage('hello from bsg.world'), recipients=[recipient0, recipient1])
        for result in results['result']:
            print('Current SMS send API result for reference {}: \n{}'.format(result['reference'], pprint.pformat(result, indent=4)))
            status = client.get_status(result['reference'])
            print('Current SMS status result for reference {}: \n{}'.format(result['reference'], pprint.pformat(status, indent=4)))
    except api.APIError as exc:
        print('Error on SMS request processing: {}'.format(pprint.pformat(exc, indent=4)), file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    main()
