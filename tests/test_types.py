# -*- coding: utf-8 -*-
'''Test WGC type results.'''
import pytest

from webgeocalc.types import ResultTypeError, get_type

def test_type_err():
    '''Test error unknown type results.'''
    with pytest.raises(ResultTypeError):
        get_type('WRONG_TYPE')
