# -*- coding: utf-8 -*-
'''Test WGC type results.'''
import pytest

from webgeocalc.vars import set_param

def test_set_param():
    '''Test error unknown type results.'''
    with pytest.raises(KeyError):
        @set_param(valid_params='WRONG_TYPE')
        def dummy(_self, val):
            pass
