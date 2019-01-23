# -*- coding: utf-8 -*-
import requests

from .vars import API_URL
from .errors import APIError, APIReponseError, TooManyKernelSets, KernelSetNotFound
from .types import get_type, ColumnResult, KernelSetDetails

class Api(object):
    '''WebGeoCalc API object'''

    def __init__(self, url=API_URL):
        self.url = url
        self._kernel_sets = None

    def get(self, url):
        '''Parsed GET request'''
        response = requests.get(self.url + url)
        if response.ok:
            return self.read(response.json())
        else:
            response.raise_for_status()

    def post(self, url, payload):
        '''Parsed POST request'''
        response = requests.post(self.url + url, json=payload)
        if response.ok:
            return self.read(response.json())
        else:
            response.raise_for_status()

    def read(self, json):
        '''Read content from json reponse'''
        if json['status'] != 'OK':
            raise APIError(json['message'])
        
        keys = json.keys()

        if 'resultType' in keys and 'items' in json:
            dtype = get_type(json['resultType'])
            return [dtype(item) for item in json['items']]

        elif 'result' in keys:
            return json['calculationId'], json['result']['phase'], json['result']['progress']

        elif 'columns' in keys and 'rows' in keys:
            cols = [ ColumnResult(col) for col in json['columns'] ]
            return cols, json['rows']
        
        else:
            raise APIReponseError(json)

    def kernel_sets(self):
        '''
            Get list of kernel sets available on the server.
            GET: /kernel-sets
        '''
        if self._kernel_sets is None:
            self._kernel_sets = self.get('/kernel-sets')
        return self._kernel_sets

    def kernel_set(self, kernel_set):
        '''Get kernel set by caption name or kernel set id'''
        kernel_sets = list(filter(lambda x: kernel_set in x, self.kernel_sets()))
        if len(kernel_sets) == 1:
            return kernel_sets[0]
        elif len(kernel_sets) > 1:
            raise TooManyKernelSets(kernel_set, kernel_sets)
        else:
            raise KernelSetNotFound(kernel_set)

    def kernel_set_id(self, kernel_set):
        if isinstance(kernel_set, int):
            return kernel_set
        elif isinstance(kernel_set, str):
            return int(self.kernel_set(kernel_set))
        elif isinstance(kernel_set, KernelSetDetails):
            return int(kernel_set)
        else:
            raise TypeError(f"'kernel_set' must be a 'int', a 'str' of a 'KernelSetDetails' object:\n' + \
                             '>>> Type({kernel_set}) = {type(kernel_set)}")

    def bodies(self, kernel_set):
        '''
            Get list of bodies available in a kernel set.
            GET: /kernel-set/{kernelSetId}/bodies
        '''
        kernelSetId = self.kernel_set_id(kernel_set)
        return self.get(f'/kernel-set/{kernelSetId}/bodies')

    def frames(self, kernel_set):
        '''
            Get list of frames available in a kernel set.
            GET: /kernel-set/{kernelSetId}/frames
        '''
        kernelSetId = self.kernel_set_id(kernel_set)
        return self.get(f'/kernel-set/{kernelSetId}/frames')

    def instruments(self, kernel_set):
        '''
            Get list of instruments available in a kernel set.
            GET: /kernel-set/{kernelSetId}/instruments
        '''
        kernelSetId = self.kernel_set_id(kernel_set)
        return self.get(f'/kernel-set/{kernelSetId}/instruments')

    def new_calculation(self, payload):
        '''
            Starts a new calculation.
            POST: /calculation/new 
        '''
        return self.post('/calculation/new', payload)

    def status_calculation(self, id):
        '''
            Gets the status of a calculation.
            GET: /calculation/{id} 
        '''
        return self.get(f'/calculation/{id}')

    def results_calculation(self, id):
        '''
            Gets the results of a calculation.
            GET: /calculation/{id}/results
        '''
        return self.get(f'/calculation/{id}/results')

# Export default API object
API = Api()
