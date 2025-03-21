"""Test WGC illumination angles calculation."""

from pytest import fixture, raises

from webgeocalc import IlluminationAngles
from webgeocalc.errors import CalculationInvalidAttr, CalculationInvalidValue


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
    """Input frame."""
    return 'IAU_ENCELADUS'


@fixture
def observer():
    """Input observer."""
    return 'CASSINI'


@fixture
def lat():
    """Input latitude."""
    return 0.0


@fixture
def lon():
    """Input longitude."""
    return 0.0


@fixture
def corr():
    """Input aberration correction."""
    return 'CN+S'


@fixture
def params(kernels, time, target, target_frame, observer, lat, lon, corr):
    """Input parameters from WGC API example."""
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


@fixture
def payload(kernels, time, target, target_frame, observer, lat, lon, corr):
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
    """Test illumination angles payload."""
    assert IlluminationAngles(**params) == payload


def test_illumination_angles_attr_error(params):
    """Test errors when illumination angles attributes are invalid."""
    with raises(CalculationInvalidAttr):
        IlluminationAngles(shape_1='POINT', **params)

    with raises(CalculationInvalidAttr):
        IlluminationAngles(coordinate_representation='WRONG', **params)


def test_illumination_angles_value_error(params):
    """Test latitude and longitude invalid inputs."""
    params['latitude'] = 100
    with raises(CalculationInvalidValue):
        IlluminationAngles(**params)

    params['latitude'] = 90
    params['longitude'] = 190
    with raises(CalculationInvalidValue):
        IlluminationAngles(**params)
