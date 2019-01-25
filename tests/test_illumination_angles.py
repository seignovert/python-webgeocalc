# -*- coding: utf-8 -*-
import pytest
import requests_mock

from webgeocalc import IlluminationAngles
from webgeocalc.errors import CalculationInvalidAttr, CalculationInvalidValue

@pytest.fixture
def kernels():
    return 5 # Cassini-Huygens

@pytest.fixture
def time():
    return '2012-10-19T08:24:00.000'

@pytest.fixture
def target():
    return 'ENCELADUS'

@pytest.fixture
def target_frame():
    return 'IAU_ENCELADUS'

@pytest.fixture
def observer():
    return 'CASSINI'

@pytest.fixture
def lat():
    return 0.0

@pytest.fixture
def lon():
    return 0.0

@pytest.fixture
def corr():
    return 'CN+S'

@pytest.fixture
def params(kernels, time, target, target_frame, observer, lat, lon, corr):
    return {
        'kernels': kernels,
        'times': time,
        'target': target,
        'target_frame': target_frame,
        'observer': observer,
        'latitude': lat,
        'longitude': lon,
        'aberration_correction': corr,
    }

@pytest.fixture
def payload(kernels, time, target, target_frame, observer, lat, lon, corr):
    return {
        "kernels": [{
            "type": "KERNEL_SET",
            "id": kernels,
        }],
        "timeSystem": "UTC",
        "timeFormat": "CALENDAR",
        "times": [
            time,
        ],
        "calculationType": "ILLUMINATION_ANGLES",
        "target": target,
        "shape1": "ELLIPSOID",
        "targetFrame": target_frame,
        "observer": observer,
        "coordinateRepresentation": "LATITUDINAL",
        "latitude": lat,
        "longitude": lon,
        "aberrationCorrection": corr,
    }

def test_illumination_angles_payload(params, payload):
    assert IlluminationAngles(**params).payload == payload

def test_illumination_angles_attr_error(params, payload):
    with pytest.raises(CalculationInvalidAttr):
        IlluminationAngles(shape_1='POINT', **params)

    with pytest.raises(CalculationInvalidAttr):
        IlluminationAngles(coordinate_representation='WRONG', **params)

def test_illumination_angles_value_error(params, payload):
    params['latitude'] = 100
    with pytest.raises(CalculationInvalidValue):
        IlluminationAngles(**params)

    params['latitude'] = 90
    params['longitude'] = 190
    with pytest.raises(CalculationInvalidValue):
        IlluminationAngles(**params)
