#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
This module generate a random number.
'''

__author__ = 'digiacom'

import json
import requests

USER_FILE = 'user.json'
URL = 'https://api.random.org/json-rpc/4/invoke'


def __load_api_key(filename: str) -> str:
    '''Load the API key from a json-formatted file.

    File must be structured like this:
    {
        "api_key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    }
    '''
    try:
        with open(filename, mode='rt', encoding='utf-8') as file:
            return json.load(file)['api_key']
    except IOError:
        print('Error opening credential file')
        raise


def __get_headers_and_payload():
    '''Helper function to generate request headers and data stubs'''
    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        'jsonrpc': '2.0',
        'method': 'generateIntegers',
        'params': {
            'n': 1
        },
        'id': 42
    }

    return (headers, payload)


def get_random_number(low: int = 1, high: int = 100) -> int:
    '''Get a random integer number between low and high.'''
    api_key = __load_api_key(USER_FILE)
    headers, payload = __get_headers_and_payload()

    payload['params']['apiKey'] = api_key
    payload['params']['min'] = low
    payload['params']['max'] = high

    resp = requests.post(URL, json=payload, headers=headers)

    if resp.status_code == 200:
        return resp.json()['result']['random']['data'][0]
    else:
        raise Exception(resp.status_code)


def get_random_day() -> int:
    '''Get a random number between 1 and 31'''
    return get_random_number(high=31)


if __name__ == '__main__':
    print(get_random_day())
    