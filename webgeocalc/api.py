# -*- coding: utf-8 -*-
import requests
import json

from .vars import API_URL
from .types import get_type

class Api(object):
    '''WebGeoCalc API object'''

    def __init__(self, url=API_URL):
        self.url = url

    def get(self, url):
        '''Parsed get request'''
        response = requests.get(self.url + url)
        if response.ok:
            return self.loads(response.content)
        else:
            response.raise_for_status()

    def loads(self, json_content):
        '''Load json content based on result type'''
        data = json.loads(json_content)
        dtype = get_type(data['resultType'])
        return [dtype(item) for item in data['items']]

    def kernel_sets(self):
        '''Get list of kernel sets available on the server.'''
        return self.get('/kernel-sets')


# Export default API object
API = Api()
