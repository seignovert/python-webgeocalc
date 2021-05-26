"""Test WGC sub observer point calculation."""

from pytest import fixture, raises

from webgeocalc import SubSolarPoint
from webgeocalc.errors import CalculationInvalidAttr


@fixture
def kernels():
    """Cassini kernel set."""
    return 5


@fixture
def time():
    """Input time."""
    return '2012-10-19T08:24:00.000'


@fixture
def target():
    """Input target."""
    return 'ENCELADUS'


@fixture
def target_frame():
    """Input target frame."""
    return 'IAU_ENCELADUS'


@fixture
def observer():
    """Input observer."""
    return 'CASSINI'


@fixture
def corr():
    """Input aberration correction."""
    return 'CN+S'


@fixture
def params(kernels, time, target, target_frame, observer, corr):
    """Input parameters from WGC API example."""
    return {
        'kernels': kernels,
        'times': time,
        'target': target,
        'target_frame': target_frame,
        'observer': observer,
        'aberration_correction': corr,
    }


@fixture
def payload(kernels, time, target, target_frame, observer, corr):
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
        "calculationType": "SUB_SOLAR_POINT",
        "target": target,
        "targetFrame": target_frame,
        "observer": observer,
        "subPointType": "Near point: ellipsoid",
        "aberrationCorrection": corr,
        "stateRepresentation": "RECTANGULAR",
    }


def test_sub_solar_point_payload(params, payload):
    """Test sub observer point payload."""
    assert SubSolarPoint(**params).payload == payload


def test_sub_solar_point_attr_error(params):
    """Test errors when sub observer point attributes are invalid."""
    with raises(CalculationInvalidAttr):
        SubSolarPoint(sub_point_type='WRONG', **params)

    del params['aberration_correction']
    with raises(CalculationInvalidAttr):
        SubSolarPoint(aberration_correction='XCN', **params)
