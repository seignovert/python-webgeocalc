# -*- coding: utf-8 -*-
import json

from .api import API
from .types import KernelSetDetails


class Calculation(object):
    '''Calculation object'''

    def __init__(self, kernel_sets=1):
        self.kernels = self.load_kernel_sets(kernel_sets)

    @property
    def payload(self):
        return json.dumps({
            "kernels": self.kernels,
        }, separators=(',', ':'))

    def load_kernel_sets(self, kernel_sets):
        '''Load one or more kernels at once'''
        if kernel_sets is None:
            return []
        if isinstance(kernel_sets, (int, str, KernelSetDetails)):
            return [self.kernel_set(kernel_sets)]
        else:
            return list(map(self.kernel_set, kernel_sets))

    def kernel_set(self, kernel_set):
        '''Add a kernel to the calculation payload'''
        kernelSetId = API.kernel_set_id(kernel_set)
        return {
            "type": "KERNEL_SET",
            "id": kernelSetId
        }

    def add_kernel_path(self, path):
        '''Add server path to the kernel as an individual kernel'''
        return self.kernels.append({
            "type": "KERNEL",
            "path": path
        })
