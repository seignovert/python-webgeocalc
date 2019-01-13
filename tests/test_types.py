# -*- coding: utf-8 -*-
import pytest

from webgeocalc.types import get_type, ResultTypeError

def test_type_err():
    with pytest.raises(ResultTypeError):
        get_type('WRONG_TYPE')
