#!/usr/bin/env python3

import sys
import os
import pprint

sys.path.append(os.path.abspath(os.sep.join([os.path.dirname(__file__), '..'])))
import bsg_restapi as api


def main():
    from examples.settings import API_KEY

    try:
        client = api.Requester(config={'api_key': API_KEY})

        print('Default API endpoint is \'{}\''.format(client.config['api_endpoint']))

        # can change global endpoint for all parent request types
        client.config['api_endpoint'] = 'https://api.bsg.hk/v1.0'
        print('Alternate API endpoint is \'{}\''.format(client.config['api_endpoint']))

        # can use client's certificate
        client.session.cert = 'client.pem'

        # can use https proxy (for debug purposes or in enterprise network), uncomment for test
        # client.session.proxies.update({'https': 'http://localhost:8080'})

        response = client.proceed('common', 'balance')
        print('Current response: \n{}'.format(pprint.pformat(response)))

    except api.APIError as exc:
        print('Error on request processing: {}'.format(pprint.pformat(exc)), file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    main()
