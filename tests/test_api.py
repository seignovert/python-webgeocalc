# -*- coding: utf-8 -*-
import pytest

from webgeocalc import API

from requests import HTTPError
from webgeocalc.vars import API_URL
from webgeocalc.types import ResultAttributeError

@pytest.fixture
def solar_system_kernel():
    return {
        'caption': 'Solar System Kernels',
        'sclkId': '0',
        'description': 'Generic kernels for planets, satellites, and some asteroids covering from 1950-01-01 to 2050-01-01.',
        'kernelSetId': '1',
        'missionId': 'gen',
    }

def test_api_default_url():
    assert API.url == API_URL

def test_kernel_sets(solar_system_kernel):
    kernel = API.kernel_sets()[0]

    assert int(kernel) == int(solar_system_kernel['kernelSetId'])
    assert str(kernel) == solar_system_kernel['caption']
    
    for key in kernel.keys():
        assert key in solar_system_kernel.keys()

    for value in kernel.values():
        assert value in solar_system_kernel.values()
    
    for key, values in kernel.items():
        assert key in solar_system_kernel.keys()
        assert value in solar_system_kernel.values()

    with pytest.raises(ResultAttributeError):
        kernel.wrong_attr


def test_response_err():
    with pytest.raises(HTTPError):
        API.get('/') # 404 error
