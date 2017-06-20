#!/usr/bin/env python3

import sys
import os
import pprint

sys.path.append(os.path.abspath(os.sep.join([os.path.dirname(__file__), '..'])))
import bsg_restapi as api


def main():
    from examples.settings import API_KEY

    try:
        client = api.BalanceAPI(config={'api_key': API_KEY})
        balance = client.get()
        print('Current balance response: \n{}'.format(pprint.pformat(balance)))
    except api.APIError as exc:
        print('Error on balance request processing: {}'.format(pprint.pformat(exc)), file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    main()
