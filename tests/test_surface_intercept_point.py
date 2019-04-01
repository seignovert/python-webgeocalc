# -*- coding: utf-8 -*-
'''Test WGC surface intercpt point calculation.'''

import pytest

from webgeocalc import SurfaceInterceptPoint
from webgeocalc.errors import CalculationInvalidAttr, CalculationUndefinedAttr

@pytest.fixture
def kernels():
    '''Cassini kernel set.'''
    return 5

@pytest.fixture
def time():
    '''Input time.'''
    return '2012-10-19T08:24:00.000'

@pytest.fixture
def target():
    '''Input target.'''
    return 'ENCELADUS'

@pytest.fixture
def target_frame():
    '''Input target frame.'''
    return 'IAU_ENCELADUS'

@pytest.fixture
def observer():
    '''Input observer.'''
    return 'CASSINI'

@pytest.fixture
def direction_vector_type_1():
    '''Input direction vector type 1.'''
    return 'INSTRUMENT_BORESIGHT'

@pytest.fixture
def direction_vector_type_2():
    '''Input direction vector type 2.'''
    return 'REFERENCE_FRAME_AXIS'

@pytest.fixture
def direction_vector_type_3():
    '''Input direction vector type 3.'''
    return 'VECTOR_IN_INSTRUMENT_FOV'

@pytest.fixture
def direction_vector_type_4():
    '''Input direction vector type 4.'''
    return 'VECTOR_IN_REFERENCE_FRAME'

@pytest.fixture
def direction_instrument():
    '''Input direction instrument.'''
    return 'CASSINI_ISS_NAC'

@pytest.fixture
def direction_frame():
    '''Input direction frame.'''
    return 'CASSINI_ISS_NAC'

@pytest.fixture
def direction_frame_axis():
    '''Input direction axis.'''
    return 'Z'

@pytest.fixture
def corr():
    '''Input aberration correction.'''
    return 'NONE'

@pytest.fixture
def state():
    '''Input state.'''
    return 'LATITUDINAL'

@pytest.fixture
def params_1(kernels, time, target, target_frame, observer, direction_vector_type_1,
             direction_instrument, corr, state):
    '''Input parameters from WGC API example 1.'''
    return {
        'kernels': kernels,
        'times': time,
        'target': target,
        'target_frame': target_frame,
        'observer': observer,
        'direction_vector_type': direction_vector_type_1,
        'direction_instrument': direction_instrument,
        'aberration_correction': corr,
        'state_representation': state,
    }

@pytest.fixture
def payload_1(kernels, time, target, target_frame, observer, direction_vector_type_1,
              direction_instrument, corr, state):
    '''Payload from WGC API example 1.'''
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
        "calculationType": "SURFACE_INTERCEPT_POINT",
        "target": target,
        "shape1": "ELLIPSOID",
        "targetFrame": target_frame,
        "observer": observer,
        "directionVectorType": direction_vector_type_1,
        "directionInstrument": direction_instrument,
        "aberrationCorrection": corr,
        "stateRepresentation": state,
    }

@pytest.fixture
def params_2(kernels, time, target, target_frame, observer, direction_vector_type_2,
             direction_frame, direction_frame_axis, corr):
    '''Input parameters from WGC API example 2.'''
    return {
        'kernels': kernels,
        'times': time,
        'target': target,
        'target_frame': target_frame,
        'observer': observer,
        'direction_vector_type': direction_vector_type_2,
        'direction_frame': direction_frame,
        'direction_frame_axis': direction_frame_axis,
        'aberration_correction': corr,
    }

@pytest.fixture
def payload_2(kernels, time, target, target_frame, observer, direction_vector_type_2,
              direction_frame, direction_frame_axis, corr):
    '''Payload from WGC API example 2.'''
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
        "calculationType": "SURFACE_INTERCEPT_POINT",
        "target": target,
        "shape1": "ELLIPSOID",
        "targetFrame": target_frame,
        "observer": observer,
        "directionVectorType": direction_vector_type_2,
        "directionFrame": direction_frame,
        "directionFrameAxis": direction_frame_axis,
        "aberrationCorrection": corr,
        "stateRepresentation": "RECTANGULAR",
    }

@pytest.fixture
def params_3(kernels, time, target, target_frame, observer, direction_vector_type_3,
             direction_instrument, corr):
    '''Input parameters from WGC API example 3.'''
    return {
        'kernels': kernels,
        'times': time,
        'target': target,
        'target_frame': target_frame,
        'observer': observer,
        'direction_vector_type': direction_vector_type_3,
        "direction_instrument": direction_instrument,
        'direction_vector_x': 0,
        'direction_vector_y': 0,
        'direction_vector_z': 1,
        'aberration_correction': corr,
    }

@pytest.fixture
def payload_3(kernels, time, target, target_frame, observer, direction_vector_type_3,
              direction_instrument, corr):
    '''Payload from WGC API example 3.'''
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
        "calculationType": "SURFACE_INTERCEPT_POINT",
        "target": target,
        "shape1": "ELLIPSOID",
        "targetFrame": target_frame,
        "observer": observer,
        "directionVectorType": direction_vector_type_3,
        "directionInstrument": direction_instrument,
        "directionVectorX": 0,
        "directionVectorY": 0,
        "directionVectorZ": 1,
        "aberrationCorrection": corr,
        "stateRepresentation": "RECTANGULAR",
    }

@pytest.fixture
def params_4(kernels, time, target, target_frame, observer, direction_vector_type_4,
             direction_frame, corr):
    '''Input parameters from WGC API example 4.'''
    return {
        'kernels': kernels,
        'times': time,
        'target': target,
        'target_frame': target_frame,
        'observer': observer,
        'direction_vector_type': direction_vector_type_4,
        "direction_frame": direction_frame,
        'direction_vector_ra': 0,
        'direction_vector_dec': 90,
        'aberration_correction': corr,
    }

@pytest.fixture
def payload_4(kernels, time, target, target_frame, observer, direction_vector_type_4,
              direction_frame, corr):
    '''Payload from WGC API example 4.'''
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
        "calculationType": "SURFACE_INTERCEPT_POINT",
        "target": target,
        "shape1": "ELLIPSOID",
        "targetFrame": target_frame,
        "observer": observer,
        "directionVectorType": direction_vector_type_4,
        "directionFrame": direction_frame,
        "directionVectorRA": 0,
        "directionVectorDec": 90,
        "aberrationCorrection": corr,
        "stateRepresentation": "RECTANGULAR",
    }


def test_surface_direction_point_payload_boresight(params_1, payload_1):
    '''Test surface direction point payload with INSTRUMENT_BORESIGHT.'''
    assert SurfaceInterceptPoint(**params_1).payload == payload_1

def test_surface_direction_point_payload_reference_frame_axis(params_2, payload_2):
    '''Test surface direction point payload with REFERENCE_FRAME_AXIS.'''
    assert SurfaceInterceptPoint(**params_2).payload == payload_2

def test_surface_direction_point_payload_vector_in_instrument_fov(params_3, payload_3):
    '''Test surface direction point payload with VECTOR_IN_INSTRUMENT_FOV.'''
    assert SurfaceInterceptPoint(**params_3).payload == payload_3

def test_surface_direction_point_payload_vector_in_reference_frame(params_4, payload_4):
    '''Test surface direction point payload with VECTOR_IN_REFERENCE_FRAME.'''
    assert SurfaceInterceptPoint(**params_4).payload == payload_4

def test_surface_direction_point_attr_error(params_1):
    '''Test errors when surface direction point attributes is invalid.'''
    with pytest.raises(CalculationInvalidAttr):
        SurfaceInterceptPoint(shape_1='POINT', **params_1)

def test_surface_direction_point_payload_vector_in_instrument_fov_err(params_3):
    '''Test errors when VECTOR_IN_INSTRUMENT_FOV is invalid.'''
    del params_3['direction_vector_x']
    with pytest.raises(CalculationUndefinedAttr):
        # Missing 'direction_vector_x'
        SurfaceInterceptPoint(**params_3)
