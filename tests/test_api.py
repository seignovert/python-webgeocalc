# -*- coding: utf-8 -*-
import pytest

from webgeocalc import API

from requests import HTTPError
from webgeocalc.vars import API_URL
from webgeocalc.errors import ResultAttributeError, TooManyKernelSets, KernelSetNotFound, APIError, APIReponseError

@pytest.fixture
def solar_system_kernel_set():
    return {
        'caption': 'Solar System Kernels',
        'sclkId': '0',
        'description': 'Generic kernels for planets, satellites, and some asteroids covering from 1950-01-01 to 2050-01-01.',
        'kernelSetId': '1',
        'missionId': 'gen',
    }

@pytest.fixture
def cassini_kernel_set():
    return {
        'caption': 'Cassini Huygens',
        'sclkId': '-82',
        'description': 'rchived CASSINI kernels covering from 1997-10-15 to 2017-09-15.',
        'kernelSetId': '5',
        'missionId': 'cassini',
    }

@pytest.fixture
def cassini_body():
    return {
        'id': -82,
        'name': 'CASSINI',
    }

@pytest.fixture
def cassini_frame():
    return {
        'id': -82905,
        'name': 'CASSINI_KSO',
        'centerBodyID': 699,
        'frameClass': 5,
    }

@pytest.fixture
def cassini_instrument():
    return {
        'id': -82898,
        'name': 'CASSINI_CIRS_RAD',
    }

@pytest.fixture
def api_error():
    return {
        "status": "ERROR",
        "message": None,
        "calculationId": "0788aba2-d4e5-4028-9ef1-4867ad5385e0"
    }

@pytest.fixture
def api_invalid_response():
    return {
        "status": "OK",
        "message": "The operation was successful.",
        "calculationId": "0788aba2-d4e5-4028-9ef1-4867ad5385e0",
    }

def test_api_default_url():
    assert API.url == API_URL
def test_response_err():
    with pytest.raises(HTTPError):
        API.get('/') # 404 error

    with pytest.raises(HTTPError):
        API.post('/', payload={}) # 404 error

def test_kernel_sets(solar_system_kernel_set):
    kernel_set = API.kernel_sets()[0]

    assert int(kernel_set) == int(solar_system_kernel_set['kernelSetId'])
    assert str(kernel_set) == solar_system_kernel_set['caption']
    
    for key in kernel_set.keys():
        assert key in solar_system_kernel_set.keys()

    for value in kernel_set.values():
        assert value in solar_system_kernel_set.values()
    
    for key, values in kernel_set.items():
        assert key in solar_system_kernel_set.keys()
        assert value in solar_system_kernel_set.values()

    with pytest.raises(ResultAttributeError):
        kernel_set.wrong_attr

def test_kernel_set_by_id():
    assert int(API.kernel_set(1)) == 1

def test_kernel_set_by_full_name():
    assert str(API.kernel_set('Solar System Kernels')) == 'Solar System Kernels'

def test_kernel_set_by_name_not_case_sensitive():
    assert str(API.kernel_set('solar system kernels')) == 'Solar System Kernels'

def test_kernel_set_by_name_partial():
    assert str(API.kernel_set('Solar')) == 'Solar System Kernels'

def test_kernel_set_too_many_found():
    with pytest.raises(TooManyKernelSets):
        assert str(API.kernel_set('Cassini'))

def test_kernel_set_not_found():
    with pytest.raises(KernelSetNotFound):
        assert str(API.kernel_set('Missing kernel'))


def test_kernel_set_id_for_str(cassini_kernel_set):
    kernel_set_id = int(cassini_kernel_set['kernelSetId'])
    kernel_set_caption = cassini_kernel_set['caption']

    assert API.kernel_set_id(kernel_set_caption) == kernel_set_id
    
    kernel_set = API.kernel_set(kernel_set_caption)
    assert API.kernel_set_id(kernel_set) == kernel_set_id

    with pytest.raises(TypeError):
        API.kernel_set_id(1.23)

def test_bodies(cassini_kernel_set, cassini_body):
    kernel_set_id = int(cassini_kernel_set['kernelSetId'])
    body = API.bodies(kernel_set_id)[0]

    assert int(body) == cassini_body['id']
    assert str(body) == cassini_body['name']

def test_frames(cassini_kernel_set, cassini_frame):
    kernel_set_id = int(cassini_kernel_set['kernelSetId'])
    frame = API.frames(kernel_set_id)[58]

    assert int(frame) == cassini_frame['id']
    assert str(frame) == cassini_frame['name']

    for value in frame.values():
        assert value in cassini_frame.values()

def test_instruments(cassini_kernel_set, cassini_instrument):
    kernel_set_id = int(cassini_kernel_set['kernelSetId'])
    instrument = API.instruments(kernel_set_id)[0]

    assert int(instrument) == cassini_instrument['id']
    assert str(instrument) == cassini_instrument['name']

def test_api_read_error(api_error):
    with pytest.raises(APIError):
        API.read(api_error)

def test_api_read_invalid(api_invalid_response):
    with pytest.raises(APIReponseError):
        API.read(api_invalid_response)
