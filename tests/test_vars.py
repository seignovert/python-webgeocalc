# -*- coding: utf-8 -*-
'''Test WGC type results.'''
import pytest

from webgeocalc.vars import get_var

def test_var_err():
    '''Test error unknown type results.'''
    with pytest.raises(KeyError):
        get_var('WRONG_TYPE')
