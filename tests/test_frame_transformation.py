"""Test WGC angular frame transformation calculation."""

from pytest import fixture, raises

from webgeocalc import FrameTransformation
from webgeocalc.errors import (CalculationIncompatibleAttr,
                               CalculationInvalidAttr)


@fixture
def kernels():
    """Cassini kernel set."""
    return 5


@fixture
def time():
    """Input time."""
    return '2012-10-19T08:24:00.000'


@fixture
def frame_1():
    """Input frame 1."""
    return 'IAU_SATURN'


@fixture
def frame_2():
    """Input frame 2."""
    return 'IAU_ENCELADUS'


@fixture
def corr():
    """Input aberration correction."""
    return 'NONE'


@fixture
def params(kernels, time, frame_1, frame_2, corr):
    """Input parameters from WGC API example."""
    return {
        'kernels': kernels,
        'times': time,
        'frame_1': frame_1,
        'frame_2': frame_2,
        'aberration_correction': corr,
    }


@fixture
def payload(kernels, time, frame_1, frame_2, corr):
    """Payload from WGC API example."""
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
    """Test angular frame transformation payload."""
    assert FrameTransformation(**params).payload == payload


def test_frame_transformation_attr_err(params):
    """Test errors when frame transformation is invalid."""
    del params['aberration_correction']
    with raises(CalculationInvalidAttr):
        # aberration_correction can not be '+S'
        FrameTransformation(aberration_correction='CN+S', **params)

    with raises(CalculationInvalidAttr):
        FrameTransformation(time_location='WRONG', **params)

    with raises(CalculationInvalidAttr):
        FrameTransformation(orientation_representation='WRONG', **params)

    with raises(CalculationInvalidAttr):
        FrameTransformation(axis_1='WRONG', **params)

    with raises(CalculationInvalidAttr):
        FrameTransformation(angular_units='WRONG', **params)

    with raises(CalculationInvalidAttr):
        FrameTransformation(angular_velocity_representation='WRONG', **params)

    with raises(CalculationInvalidAttr):
        FrameTransformation(angular_velocity_units='WRONG', **params)

    with raises(CalculationIncompatibleAttr):
        FrameTransformation(angular_velocity_representation='EULER_ANGLE_DERIVATIVES',
                            angular_velocity_units='Unitary', **params)
