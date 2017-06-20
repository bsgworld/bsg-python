#!/usr/bin/env python3

import sys
import os
import pprint

sys.path.append(os.path.abspath(os.sep.join([os.path.dirname(__file__), '..'])))
import bsg_restapi as api


def main():
    from examples.settings import API_KEY

    try:
        client = api.ViberAPI(config={'api_key': API_KEY})
        prices = client.get_prices()
        print('Viber Prices (first 5 elements from {}): \n{}'
              .format(len(prices), pprint.pformat(prices[0:5], indent=4)))

        recipient = api.Recipient(380967000000)
        print('Created recipient: \n{}'.format(pprint.pformat(recipient)))

        client.add_message(api.ViberMessage(to=[recipient], text='message text from BSG REST API'))

        result = client.send()
        print('Current Viber send API result: \n{}'.format(pprint.pformat(result, indent=4)))
        status = client.get_status(result['result'][0]['reference'])
        print('Current Viber status result: \n{}\n'.format(pprint.pformat(status, indent=4)))

        client.clear_messages()
        recipient0 = api.Recipient(380967000000)
        recipient1 = api.Recipient(380967000001)
        print('Created another one recipients: \n{}'.format(pprint.pformat([recipient0, recipient1])))
        client.add_message(
            api.ViberMessage(
                to=[recipient0, recipient1],
                text='another message text from BSG REST API'))
        results = client.send()
        for result in results['result']:
            print('Current Viber send API result for reference {}: \n{}'
                  .format(result['reference'], pprint.pformat(result, indent=4)))
            status = client.get_status(result['reference'])
            print('Current Viber status result for reference {}: \n{}'
                  .format(result['reference'], pprint.pformat(status, indent=4)))

        result = client.send(
            api.ViberMessage(
                to=[api.Recipient(380967000000)],
                alt_route=dict(originator='BSG', text='sms message text from viber alt_route'),
                text='viber message text from BSG REST API'))
        result = result['result'][0]
        print('Current Viber send API result for reference {}: \n{}'
              .format(result['reference'], pprint.pformat(result, indent=4)))
        status = client.get_status(result['reference'])
        print('Current Viber status result for reference {}: \n{}'
              .format(result['reference'], pprint.pformat(status, indent=4)))

        # can request status for any previously received reference
        reference = 'f32d63d1'
        status = client.get_status(reference)
        print('Current Viber status result for reference {}: \n{}'
              .format(reference, pprint.pformat(status, indent=4)))

    except api.APIError as exc:
        print('Error on Viber request processing: {}'.format(pprint.pformat(exc, indent=4)), file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    main()
