BSG REST API Wrapper for Python
================================

This repository contains the open source Python client for BSG REST API.


Requirements
------------

For access to BSG API:
- [Sign up](https://bsg.world) for a free account
- Get `api_key`
- Python 3.2+, [requests](https://pypi.python.org/pypi/requests)

For development:
- [pytest](https://pypi.python.org/pypi/pytest)


Installation
------------
[Download](https://github.com/bsgworld/bsg-python/archive/master.zip) repository, decompress, install with
`setup.py install`

Usage
-----
See [BSG REST API Documentation](https://bsg.world/developers/rest-api/) for complete list of API clients, error codes, result codes etc.

An short example of a SMS API usage:
```python
import pprint
import bsg_restapi as api
from examples.settings import API_KEY

client = api.SMSAPI(config={'api_key': API_KEY})
result = client.send(message=api.SMSMessage(body='test message text'), recipients=api.Recipient(380967770002))
print('Result of SMS sending:\n{}'.format(pprint.pformat(result)))
# getting status of SMS
status = client.get_status(result['reference'])
print('Current SMS status result for reference {}: \n{}'.format(result['reference'], pprint.pformat(status, indent=4)))
```

An example of a HLR API usage:
```python
import pprint
import bsg_restapi as api
from examples.settings import API_KEY

# Create HLR API Client
client = api.HLRAPI(config={'api_key': API_KEY})

# Get prices for HLR
prices = client.get_prices()
print('HLR Prices (first 5 elements from {}): \n{}'.format(len(prices), pprint.pformat(prices[0:5], indent=4)))

# Get HLR for single smisdn:
lookup_list = api.HLRL(380970000000)
print('Created HLR request: \n{}'.format(pprint.pformat(lookup_list, indent=4)))
# Send the request
result = client.send(lookup_list)
# Get server response
result_id = result['result'][0]['id']
# Get status of HLR by result_id:
status_id = client.get_status(result_id)
# Try the same for 'reference'
result_ref = result['result'][0]['reference']
status_ref = client.get_status(result_ref)
# and print the result
print('Current HLR response by id: \n{}'.format(pprint.pformat(status_id, indent=4)))
print('Current HLR response by reference: \n{}'.format(pprint.pformat(status_ref, indent=4)))
```

See [examples](examples) subfolder for
- samples of usage,
- various API processing and error handling aspects,
- examples for client's SSL certificate and proxy usage.
