# -*- coding: utf-8 -*-
'''Test WGC API base urls.'''

import pytest

from requests import HTTPError

from webgeocalc import API
from webgeocalc.errors import (APIError, APIReponseError, KernelSetNotFound,
                               ResultAttributeError, TooManyKernelSets)
from webgeocalc.vars import API_URL

@pytest.fixture
def solar_system_kernel_set():
    '''Solar kernels API output.'''
    return {
        'caption': 'Solar System Kernels',
        'sclkId': '0',
        'description': 'Generic kernels for planets, satellites, and some asteroids '
                       'covering from 1950-01-01 to 2050-01-01.',
        'kernelSetId': '1',
        'missionId': 'gen',
    }

@pytest.fixture
def cassini_kernel_set():
    '''Cassini kernel API output.'''
    return {
        'caption': 'Cassini Huygens',
        'sclkId': '-82',
        'description': 'Archived CASSINI kernels covering from 1997-10-15 to 2017-09-15.',
        'kernelSetId': '5',
        'missionId': 'cassini',
    }

@pytest.fixture
def cassini_body():
    '''Cassini body API output.'''
    return {
        'id': -82,
        'name': 'CASSINI',
    }

@pytest.fixture
def cassini_frame():
    '''Cassini frame API output.'''
    return {
        'id': -82905,
        'name': 'CASSINI_KSO',
        'centerBodyID': 699,
        'frameClass': 5,
    }

@pytest.fixture
def cassini_instrument():
    '''CIRS instrument API output.'''
    return {
        'id': -82898,
        'name': 'CASSINI_CIRS_RAD',
    }

@pytest.fixture
def api_queued():
    '''Queued API response.'''
    return {
        "status": "OK",
        "message": "The request was successful.",
        "calculationId": "0788aba2-d4e5-4028-9ef1-4867ad5385e0",
        "result": {
            "phase": "QUEUED",
            "position": 6
        }
    }

@pytest.fixture
def api_error():
    '''Error API reponse.'''
    return {
        "status": "ERROR",
        "message": "The request has failed.",
        "calculationId": "0788aba2-d4e5-4028-9ef1-4867ad5385e0",
        "error": {
            "shortDescription": "The provided Calculation ID does not "
                                "correspond to any requested calculation."
        }
    }

@pytest.fixture
def api_empty_data_response():
    '''Empty data API response.'''
    return {
        "status": "OK",
        "message": "The operation was successful.",
        "calculationId": "0788aba2-d4e5-4028-9ef1-4867ad5385e0",
    }

def test_api_default_url():
    '''Test default API url.'''
    assert API.url == API_URL

def test_response_err():
    '''Test GET and POST on invalid URLs.'''
    with pytest.raises(HTTPError):
        API.get('/')  # 404 error

    with pytest.raises(HTTPError):
        API.post('/', payload={})  # 404 error

def test_kernel_sets(solar_system_kernel_set):
    '''Test GET kernel sets from API.'''
    kernel_set = API.kernel_sets()[0]

    assert int(kernel_set) == int(solar_system_kernel_set['kernelSetId'])
    assert str(kernel_set) == solar_system_kernel_set['caption']

    for key in kernel_set.keys():
        assert key in solar_system_kernel_set.keys()

    for value in kernel_set.values():
        assert value in solar_system_kernel_set.values()

    for key, value in kernel_set.items():
        assert key in solar_system_kernel_set.keys()
        assert value in solar_system_kernel_set.values()

    with pytest.raises(ResultAttributeError):
        _ = kernel_set.wrong_attr

def test_kernel_set_by_id():
    '''Test kernel set id.'''
    assert int(API.kernel_set(1)) == 1

def test_kernel_set_by_full_name():
    '''Test kernel set name.'''
    assert str(API.kernel_set('Solar System Kernels')) == 'Solar System Kernels'

def test_kernel_set_by_name_not_case_sensitive():
    '''Test case sensitivity of kernel set search.'''
    assert str(API.kernel_set('solar system kernels')) == 'Solar System Kernels'

def test_kernel_set_by_name_partial():
    '''Test partial kernel set search.'''
    assert str(API.kernel_set('Solar')) == 'Solar System Kernels'

def test_kernel_set_too_many_found():
    '''Test error if too many kernel sets are found.'''
    with pytest.raises(TooManyKernelSets):
        assert str(API.kernel_set('Cassini'))

def test_kernel_set_not_found():
    '''Test error if kernel set not found.'''
    with pytest.raises(KernelSetNotFound):
        assert str(API.kernel_set('Missing kernel'))


def test_kernel_set_id_for_str(cassini_kernel_set):
    '''Test kernel set search for id and error cases.'''
    kernel_set_id = int(cassini_kernel_set['kernelSetId'])
    kernel_set_caption = cassini_kernel_set['caption']

    assert API.kernel_set_id(kernel_set_caption) == kernel_set_id

    kernel_set = API.kernel_set(kernel_set_caption)
    assert API.kernel_set_id(kernel_set) == kernel_set_id

    with pytest.raises(TypeError):
        API.kernel_set_id(1.23)

def test_bodies(cassini_kernel_set, cassini_body):
    '''Test GET bodies from API.'''
    kernel_set_id = int(cassini_kernel_set['kernelSetId'])
    body = API.bodies(kernel_set_id)[0]

    assert int(body) == cassini_body['id']
    assert str(body) == cassini_body['name']

def test_frames(cassini_kernel_set, cassini_frame):
    '''Test GET frames from API.'''
    kernel_set_id = int(cassini_kernel_set['kernelSetId'])
    frame = API.frames(kernel_set_id)[58]

    assert int(frame) == cassini_frame['id']
    assert str(frame) == cassini_frame['name']

    for value in frame.values():
        assert value in cassini_frame.values()

def test_instruments(cassini_kernel_set, cassini_instrument):
    '''Test GET instruments from API.'''
    kernel_set_id = int(cassini_kernel_set['kernelSetId'])
    instrument = API.instruments(kernel_set_id)[0]

    assert int(instrument) == cassini_instrument['id']
    assert str(instrument) == cassini_instrument['name']


def test_api_read_queued(api_queued):
    '''Test queued position output from API.'''
    _, phase = API.read(api_queued)
    assert phase == 'QUEUED | POSITION: 6'

def test_api_read_error(api_error):
    '''Test error output from API.'''
    with pytest.raises(APIError):
        API.read(api_error)

def test_api_read_invalid(api_empty_data_response):
    '''Test error if response no valid data.'''
    with pytest.raises(APIReponseError):
        API.read(api_empty_data_response)
