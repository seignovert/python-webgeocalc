"""Test WGC angular separation calculation."""

from pytest import fixture, raises
from pytest import mark

from webgeocalc import AngularSeparation
from webgeocalc.direction import Direction
from webgeocalc.errors import CalculationInvalidAttr, CalculationRequiredAttr


@fixture
def kernel_paths():
    """Input kernel paths."""
    return [
        'pds/wgc/kernels/lsk/naif0012.tls',
        'pds/wgc/kernels/spk/de430.bsp',
    ]


@fixture
def time():
    """Input time."""
    return '2012-10-19T08:24:00.000'


@fixture
def target_1():
    """Input name for the first target."""
    return 'VENUS'


@fixture
def target_2():
    """Input name for the second target."""
    return 'MERCURY'


@fixture
def observer():
    """Input name of the observer."""
    return 'SUN'


@fixture
def corr():
    """Input aberration correction."""
    return 'NONE'


@fixture
def params_two_targets(kernel_paths, time, target_1, target_2, observer, corr):
    """Input parameters from WGC API example (TWO_TARGETS mode)."""
    return {
        'kernel_paths': kernel_paths,
        'times': time,
        'target_1': target_1,
        'target_2': target_2,
        'observer': observer,
        'aberration_correction': corr,
    }


@fixture
def payload_two_targets(kernel_paths, time, target_1, target_2, observer, corr):
    """Payload from WGC API example (TWO_TARGETS mode)."""
    return {
        "kernels": [{
            "type": "KERNEL",
            "path": kernel_paths[0],
        }, {
            "type": "KERNEL",
            "path": kernel_paths[1],
        }],
        "timeSystem": "UTC",
        "timeFormat": "CALENDAR",
        "times": [time],
        "calculationType": "ANGULAR_SEPARATION",
        "target1": target_1,
        "shape1": "POINT",
        "target2": target_2,
        "shape2": "POINT",
        "observer": observer,
        "aberrationCorrection": corr
    }


@fixture
def kernel_set():
    """Input kernel set."""
    return 5


@fixture
def direction_position():
    """Input position direction as dict object."""
    return {
        "direction_type": "POSITION",
        "target": "SUN",
        "shape": "POINT",
        "observer": "CASSINI"
    }


@fixture
def direction_position_payload():
    """Position direction payload."""
    return {
        'aberrationCorrection': 'NONE',
        'antiVectorFlag': False,
        "directionType": "POSITION",
        "target": "SUN",
        "shape": "POINT",
        "observer": "CASSINI"
    }


@fixture
def direction_vector():
    """Input vector direction as Direction object."""
    return Direction(
        direction_type='VECTOR',
        direction_vector_type='REFERENCE_FRAME_AXIS',
        direction_frame='CASSINI_RPWS_EDIPOLE',
        direction_frame_axis='Z',
    )


@fixture
def direction_vector_payload():
    """Vector direction payload."""
    return {
        'aberrationCorrection': 'NONE',
        'antiVectorFlag': False,
        "directionType": "VECTOR",
        "directionVectorType": "REFERENCE_FRAME_AXIS",
        "directionFrame": "CASSINI_RPWS_EDIPOLE",
        "directionFrameAxis": "Z"
    }


@fixture
def params_two_directions(
        kernel_set, time, direction_vector,
        direction_position,
):
    """Input parameters for TWO_DIRECTIONS mode."""
    return {
        'spec_type': 'TWO_DIRECTIONS',
        'kernels': kernel_set,
        'times': time,
        'direction_1': direction_vector,
        'direction_2': direction_position,
    }


@fixture
def payload_two_directions(
        kernel_set, time, direction_vector_payload,
        direction_position_payload,
):
    """Input parameters for TWO_DIRECTIONS mode."""
    return {
        "kernels": [{
            "type": "KERNEL_SET",
            "id": kernel_set,
        }],
        "specType": "TWO_DIRECTIONS",
        "timeSystem": "UTC",
        "timeFormat": "CALENDAR",
        "times": [time],
        "calculationType": "ANGULAR_SEPARATION",
        "direction1": direction_vector_payload,
        "direction2": direction_position_payload,
    }


@mark.parametrize('spec_type', [
    ('TWO_TARGETS'),
    ('TWO_DIRECTIONS'),
])
def test_angular_separation_payload(request, spec_type):
    """Test angular separation payload."""
    params = request.getfixturevalue(f'params_{spec_type.lower()}')
    payload = request.getfixturevalue(f'payload_{spec_type.lower()}')

    assert AngularSeparation(**params).payload == payload


def test_angular_separation_errors(params_two_targets, params_two_directions,
                                   kernel_set, time):
    """Test angular separation payload errors."""
    # Missing observer for TWO_TARGETS
    params_two_targets.pop('observer')
    with raises(CalculationRequiredAttr):
        AngularSeparation(**params_two_targets)

    # Missing direction_1 for TWO_DIRECTIONS
    params_two_directions.pop('direction_1')
    with raises(CalculationRequiredAttr):
        AngularSeparation(**params_two_directions)

    # Invalid spec_type value
    with raises(CalculationInvalidAttr):
        AngularSeparation(kernels=kernel_set, times=time, spec_type='WRONG')
