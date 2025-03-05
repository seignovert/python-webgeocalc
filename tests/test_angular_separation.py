"""Test WGC angular separation calculation."""

from pytest import fixture

from webgeocalc import AngularSeparation


@fixture
def kernel_paths():
    """Input kernel paths."""
    return [
        'pds/wgc/kernels/lsk/naif0012.tls',
        'pds/wgc/kernels/spk/de430.bsp',
    ]


@fixture
def kernels():
    """Input kernel set."""
    return 5


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
def params(kernel_paths, time, target_1, target_2, observer, corr):
    """Input parameters from WGC API example."""
    return {
        'kernel_paths': kernel_paths,
        'times': time,
        'target_1': target_1,
        'target_2': target_2,
        'observer': observer,
        'aberration_correction': corr,
    }


@fixture
def payload(kernel_paths, time, target_1, target_2, observer, corr):
    """Payload from WGC API example."""
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
        "times": [
            time,
        ],
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
def direction_1():
    """Input first direction."""
    return {
        "direction_type": "VECTOR",
        "direction_vector_type": "REFERENCE_FRAME_AXIS",
        "direction_frame": "CASSINI_RPWS_EDIPOLE",
        "direction_frame_axis": "Z"
    }


@fixture
def direction1_payload():
    """First direction payload."""
    return {
        'aberrationCorrection': 'NONE',
        'antiVectorFlag': False,
        "directionType": "VECTOR",
        "directionVectorType": "REFERENCE_FRAME_AXIS",
        "directionFrame": "CASSINI_RPWS_EDIPOLE",
        "directionFrameAxis": "Z"
    }


@fixture
def direction_2():
    """Input second direction."""
    return {
        "direction_type": "POSITION",
        "target": "SUN",
        "shape": "POINT",
        "observer": "CASSINI"
    }


@fixture
def direction2_payload():
    """Input second direction."""
    return {
        'aberrationCorrection': 'NONE',
        'antiVectorFlag': False,
        "directionType": "POSITION",
        "target": "SUN",
        "shape": "POINT",
        "observer": "CASSINI"
    }


@fixture
def params_two_directions(kernel_set, time, direction_1, direction_2, corr):
    """Input parameters from WGC API example."""
    return {
        'spec_type': 'TWO_DIRECTIONS',
        'kernels': kernel_set,
        'times': time,
        'direction_1': direction_1,
        'direction_2': direction_2,
        'aberration_correction': corr
    }


@fixture
def payload_two_directions(kernel_set, time, direction1_payload, direction2_payload,
                           corr):
    """Input parameters from WGC API example."""
    return {
        "kernels": [{
            "type": "KERNEL_SET",
            "id": kernel_set,
        }],
        "specType": "TWO_DIRECTIONS",
        "timeSystem": "UTC",
        "timeFormat": "CALENDAR",
        "times": [
            time,
        ],
        "calculationType": "ANGULAR_SEPARATION",
        "direction1": direction1_payload,
        "direction2": direction2_payload,
        "aberrationCorrection": corr
    }


def test_angular_separation_payload(params, payload):
    """Test angular separation payload."""
    assert AngularSeparation(**params).payload == payload


def test_angular_separation_payload_two_directions(
        params_two_directions,
        payload_two_directions
):
    """Test angular separation payload (`TWO_DIRECTIONS` mode)."""
    assert AngularSeparation(**params_two_directions).payload == payload_two_directions
