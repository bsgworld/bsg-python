#!/usr/bin/env python3

import sys
import os
import pprint

sys.path.append(os.path.abspath(os.sep.join([os.path.dirname(__file__), '..'])))
import bsg_restapi as api


def main():
    from examples.settings import API_KEY

    try:
        client = api.HLRAPI(config={'api_key': API_KEY})
        prices = client.get_prices()
        print('HLR Prices (first 5 elements from {}): \n{}'.format(len(prices), pprint.pformat(prices[0:5], indent=4)))
        lookup_list = api.HLRL(380970000000)
        print('Created HLR request: \n{}'.format(pprint.pformat(lookup_list, indent=4)))
        result = client.send(lookup_list)
        result_id = result['result'][0]['id']
        status_id = client.get_status(result_id)
        result_ref = result['result'][0]['reference']
        status_ref = client.get_status(result_ref)
        print('Current HLR response by id: \n{}'.format(pprint.pformat(status_id, indent=4)))
        print('Current HLR response by reference: \n{}'.format(pprint.pformat(status_ref, indent=4)))
    except api.APIError as exc:
        print('Error on HLR request processing: {}'.format(pprint.pformat(exc, indent=4)), file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    main()
