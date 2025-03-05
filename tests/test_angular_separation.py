"""Test WGC angular separation calculation."""

from pytest import fixture
from pytest import raises

from webgeocalc.errors import CalculationInvalidAttr
from webgeocalc import AngularSeparation


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
def direction_vector_inst_boresight():
    """Input vector direction."""
    return {
        "direction_type": "VECTOR",
        "direction_vector_type": "INSTRUMENT_BORESIGHT",
        "direction_instrument": "CASSINI_ISS_NAC",
    }


@fixture
def direction_vector_inst_boresight_payload():
    """Vector direction payload."""
    return {
        'aberrationCorrection': 'NONE',
        'antiVectorFlag': False,
        "directionType": "VECTOR",
        "directionVectorType": "INSTRUMENT_BORESIGHT",
        "directionInstrument": "CASSINI_ISS_NAC",
    }


@fixture
def direction_vector_ref_frame_axis():
    """Input vector direction."""
    return {
        "direction_type": "VECTOR",
        "direction_vector_type": "REFERENCE_FRAME_AXIS",
        "direction_frame": "CASSINI_RPWS_EDIPOLE",
        "direction_frame_axis": "Z"
    }


@fixture
def direction_vector_ref_frame_axis_payload():
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
def direction_vector_in_ref_frame_xyz():
    """Input vector direction."""
    return {
        "direction_type": "VECTOR",
        "direction_vector_type": "VECTOR_IN_REFERENCE_FRAME",
        "direction_frame": "CASSINI_RPWS_EDIPOLE",
        "direction_vector_x": 0.0,
        "direction_vector_y": 0.0,
        "direction_vector_z": 1.0,
    }


@fixture
def direction_vector_in_ref_frame_xyz_payload():
    """Vector direction payload."""
    return {
        'aberrationCorrection': 'NONE',
        'antiVectorFlag': False,
        "directionType": "VECTOR",
        "directionVectorType": "VECTOR_IN_REFERENCE_FRAME",
        "directionFrame": "CASSINI_RPWS_EDIPOLE",
        "directionVectorX": 0.0,
        "directionVectorY": 0.0,
        "directionVectorZ": 1.0,
    }


@fixture
def direction_vector_in_ref_frame_radec():
    """Input vector direction."""
    return {
        "direction_type": "VECTOR",
        "direction_vector_type": "VECTOR_IN_REFERENCE_FRAME",
        "direction_frame": "CASSINI_RPWS_EDIPOLE",
        "direction_vector_ra": 0.0,
        "direction_vector_dec": 0.0,
    }


@fixture
def direction_vector_in_ref_frame_radec_payload():
    """Vector direction payload."""
    return {
        'aberrationCorrection': 'NONE',
        'antiVectorFlag': False,
        "directionType": "VECTOR",
        "directionVectorType": "VECTOR_IN_REFERENCE_FRAME",
        "directionFrame": "CASSINI_RPWS_EDIPOLE",
        "directionVectorRA": 0.0,
        "directionVectorDec": 0.0,
    }




@fixture
def direction_vector_in_ref_frame_azel():
    """Input vector direction."""
    return {
        "direction_type": "VECTOR",
        "direction_vector_type": "VECTOR_IN_REFERENCE_FRAME",
        "direction_frame": "CASSINI_RPWS_EDIPOLE",
        "direction_vector_az": 0.0,
        "direction_vector_el": 0.0,
        "azccw_flag": True,
        "elplsz_flag": True,
    }


@fixture
def direction_vector_in_ref_frame_azel_payload():
    """Vector direction payload."""
    return {
        'aberrationCorrection': 'NONE',
        'antiVectorFlag': False,
        "directionType": "VECTOR",
        "directionVectorType": "VECTOR_IN_REFERENCE_FRAME",
        "directionFrame": "CASSINI_RPWS_EDIPOLE",
        "directionVectorAz": 0.0,
        "directionVectorEl": 0.0,
        "azccwFlag": True,
        "elplszFlag": True,
    }


@fixture
def direction_velocity():
    """Input velocity direction."""
    return {
        "direction_type": "VELOCITY",
        "target": "CASSINI",
        "reference_frame": "IAU_SATURN",
        "observer": "SATURN"
    }


@fixture
def direction_velocity_payload():
    """Vector direction payload."""
    return {
        'aberrationCorrection': 'NONE',
        'antiVectorFlag': False,
        "directionType": "VELOCITY",
        "target": "CASSINI",
        "referenceFrame": "IAU_SATURN",
        "observer": "SATURN"
    }


@fixture
def direction_position():
    """Input position direction."""
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
def direction_position_anti_vector_flag_invalid():
    """Input position direction."""
    return {
        "direction_type": "POSITION",
        "target": "SUN",
        "shape": "POINT",
        "observer": "CASSINI",
        "anti_vector_flag": "Test"
    }

@fixture
def params_two_directions_anti_vector_flag_invalid(
        kernel_set, time, direction_position_anti_vector_flag_invalid,
        direction_position, corr
):
    """Input parameters for with invalid anti-vector-flag."""
    return {
        'spec_type': 'TWO_DIRECTIONS',
        'kernels': kernel_set,
        'times': time,
        'direction_1': direction_position_anti_vector_flag_invalid,
        'direction_2': direction_position,
        'aberration_correction': corr
    }


@fixture
def params_two_directions_1(
        kernel_set, time, direction_vector_ref_frame_axis,
        direction_position, corr
):
    """Input parameters from WGC API example."""
    return {
        'spec_type': 'TWO_DIRECTIONS',
        'kernels': kernel_set,
        'times': time,
        'direction_1': direction_vector_ref_frame_axis,
        'direction_2': direction_position,
        'aberration_correction': corr
    }


@fixture
def payload_two_directions_1(
        kernel_set, time, direction_vector_ref_frame_axis_payload,
        direction_position_payload, corr
):
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
        "direction1": direction_vector_ref_frame_axis_payload,
        "direction2": direction_position_payload,
        "aberrationCorrection": corr
    }


@fixture
def params_two_directions_2(
        kernel_set, time, direction_velocity,
        direction_position, corr
):
    """Input parameters from WGC API example."""
    return {
        'spec_type': 'TWO_DIRECTIONS',
        'kernels': kernel_set,
        'times': time,
        'direction_1': direction_velocity,
        'direction_2': direction_position,
        'aberration_correction': corr
    }


@fixture
def payload_two_directions_2(
        kernel_set, time, direction_velocity_payload,
        direction_position_payload, corr
):
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
        "direction1": direction_velocity_payload,
        "direction2": direction_position_payload,
        "aberrationCorrection": corr
    }


@fixture
def params_two_directions_3(
        kernel_set, time, direction_vector_inst_boresight,
        direction_position, corr
):
    """Input parameters from WGC API example."""
    return {
        'spec_type': 'TWO_DIRECTIONS',
        'kernels': kernel_set,
        'times': time,
        'direction_1': direction_vector_inst_boresight,
        'direction_2': direction_position,
        'aberration_correction': corr
    }


@fixture
def payload_two_directions_3(
        kernel_set, time, direction_vector_inst_boresight_payload,
        direction_position_payload, corr
):
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
        "direction1": direction_vector_inst_boresight_payload,
        "direction2": direction_position_payload,
        "aberrationCorrection": corr
    }


@fixture
def params_two_directions_4(
        kernel_set, time,
        direction_vector_in_ref_frame_xyz,
        direction_position, corr
):
    """Input parameters from WGC API example."""
    return {
        'spec_type': 'TWO_DIRECTIONS',
        'kernels': kernel_set,
        'times': time,
        'direction_1': direction_vector_in_ref_frame_xyz,
        'direction_2': direction_position,
        'aberration_correction': corr
    }


@fixture
def payload_two_directions_4(
        kernel_set, time, direction_vector_in_ref_frame_xyz_payload,
        direction_position_payload, corr
):
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
        "direction1": direction_vector_in_ref_frame_xyz_payload,
        "direction2": direction_position_payload,
        "aberrationCorrection": corr
    }


@fixture
def params_two_directions_5(
        kernel_set, time,
        direction_vector_in_ref_frame_radec,
        direction_position, corr
):
    """Input parameters from WGC API example."""
    return {
        'spec_type': 'TWO_DIRECTIONS',
        'kernels': kernel_set,
        'times': time,
        'direction_1': direction_vector_in_ref_frame_radec,
        'direction_2': direction_position,
        'aberration_correction': corr
    }


@fixture
def payload_two_directions_5(
        kernel_set, time, direction_vector_in_ref_frame_radec_payload,
        direction_position_payload, corr
):
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
        "direction1": direction_vector_in_ref_frame_radec_payload,
        "direction2": direction_position_payload,
        "aberrationCorrection": corr
    }


@fixture
def params_two_directions_6(
        kernel_set, time,
        direction_vector_in_ref_frame_azel,
        direction_position, corr
):
    """Input parameters from WGC API example."""
    return {
        'spec_type': 'TWO_DIRECTIONS',
        'kernels': kernel_set,
        'times': time,
        'direction_1': direction_vector_in_ref_frame_azel,
        'direction_2': direction_position,
        'aberration_correction': corr
    }


@fixture
def payload_two_directions_6(
        kernel_set, time, direction_vector_in_ref_frame_azel_payload,
        direction_position_payload, corr
):
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
        "direction1": direction_vector_in_ref_frame_azel_payload,
        "direction2": direction_position_payload,
        "aberrationCorrection": corr
    }


def test_angular_separation_payload(params, payload):
    """Test angular separation payload."""
    assert AngularSeparation(**params).payload == payload


def test_angular_separation_payload_two_directions_1(
        params_two_directions_1,
        payload_two_directions_1
):
    """Test angular separation payload (`TWO_DIRECTIONS` mode)."""
    assert AngularSeparation(**params_two_directions_1).payload == payload_two_directions_1


def test_angular_separation_payload_two_directions_1_anti_vector_flag_error(
    params_two_directions_anti_vector_flag_invalid
):
    """Test anti-vector flag error."""
    with raises(CalculationInvalidAttr):
        AngularSeparation(**params_two_directions_anti_vector_flag_invalid)

def test_angular_separation_payload_two_directions_2(
        params_two_directions_2,
        payload_two_directions_2
):
    """Test angular separation payload (`TWO_DIRECTIONS` mode)."""
    assert AngularSeparation(**params_two_directions_2).payload == payload_two_directions_2


def test_angular_separation_payload_two_directions_3(
        params_two_directions_3,
        payload_two_directions_3
):
    """Test angular separation payload (`TWO_DIRECTIONS` mode)."""
    assert AngularSeparation(**params_two_directions_3).payload == payload_two_directions_3


def test_angular_separation_payload_two_directions_4(
        params_two_directions_4,
        payload_two_directions_4
):
    """Test angular separation payload (`TWO_DIRECTIONS` mode)."""
    assert AngularSeparation(**params_two_directions_4).payload == payload_two_directions_4


def test_angular_separation_payload_two_directions_5(
        params_two_directions_5,
        payload_two_directions_5
):
    """Test angular separation payload (`TWO_DIRECTIONS` mode)."""
    assert AngularSeparation(**params_two_directions_5).payload == payload_two_directions_5


def test_angular_separation_payload_two_directions_6(
        params_two_directions_6,
        payload_two_directions_6
):
    """Test angular separation payload (`TWO_DIRECTIONS` mode)."""
    assert AngularSeparation(**params_two_directions_6).payload == payload_two_directions_6
