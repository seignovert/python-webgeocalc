# -*- coding: utf-8 -*-
import requests
import json

from .vars import API_URL
from .errors import TooManyKernelSets, KernelSetNotFound
from .types import get_type

class Api(object):
    '''WebGeoCalc API object'''

    def __init__(self, url=API_URL):
        self.url = url
        self._kernel_sets = None

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
        if self._kernel_sets is None:
            self._kernel_sets = self.get('/kernel-sets')
        return self._kernel_sets

    def kernel(self, name):
        '''Get kernel by caption'''
        kernels = list(filter(lambda x: name in x, self.kernel_sets()))
        if len(kernels) == 1:
            return kernels[0]
        elif len(kernels) > 1:
            raise TooManyKernelSets(name, kernels)
        else:
            raise KernelSetNotFound(name)

# Export default API object
API = Api()
