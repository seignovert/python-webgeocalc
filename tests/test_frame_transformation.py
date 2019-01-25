# -*- coding: utf-8 -*-
import pytest
import requests_mock

from webgeocalc import FrameTransformation
from webgeocalc.errors import CalculationInvalidAttr, CalculationIncompatibleAttr

@pytest.fixture
def kernels():
    return 5 # Cassini-Huygens

@pytest.fixture
def time():
    return '2012-10-19T08:24:00.000'

@pytest.fixture
def frame_1():
    return 'IAU_SATURN'

@pytest.fixture
def frame_2():
    return 'IAU_ENCELADUS'

@pytest.fixture
def corr():
    return 'NONE'

@pytest.fixture
def params(kernels, time, frame_1, frame_2, corr):
    return {
        'kernels': kernels,
        'times': time,
        'frame_1': frame_1,
        'frame_2': frame_2,
        'aberration_correction': corr,
    }

@pytest.fixture
def payload(kernels, time, frame_1, frame_2, corr):
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
        "calculationType": "FRAME_TRANSFORMATION",
        "frame1": frame_1,
        "frame2": frame_2,
        "aberrationCorrection": corr,
        "timeLocation": "FRAME1",
        "orientationRepresentation": "EULER_ANGLES",
        "axis1": "X",
        "axis2": "Y",
        "axis3": "Z",
        "angularUnits": "deg",
        "angularVelocityRepresentation": "VECTOR_IN_FRAME1",
        "angularVelocityUnits": "deg/s"
    }

def test_frame_transformation_payload(params, payload):
    assert FrameTransformation(**params).payload == payload

def test_frame_transformation_attr_err(params, payload):
    del params['aberration_correction']
    with pytest.raises(CalculationInvalidAttr):
        FrameTransformation(aberration_correction='CN+S', **params)

    with pytest.raises(CalculationInvalidAttr):
        FrameTransformation(time_location='WRONG', **params)

    with pytest.raises(CalculationInvalidAttr):
        FrameTransformation(orientation_representation='WRONG', **params)

    with pytest.raises(CalculationInvalidAttr):
        FrameTransformation(axis_1='WRONG', **params)

    with pytest.raises(CalculationInvalidAttr):
        FrameTransformation(angular_units='WRONG', **params)

    with pytest.raises(CalculationInvalidAttr):
        FrameTransformation(angular_velocity_representation='WRONG', **params)

    with pytest.raises(CalculationInvalidAttr):
        FrameTransformation(angular_velocity_units='WRONG', **params)

    with pytest.raises(CalculationIncompatibleAttr):
        FrameTransformation(angular_velocity_representation='EULER_ANGLE_DERIVATIVES',
                            angular_velocity_units='Unitary', **params)
