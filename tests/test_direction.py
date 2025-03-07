"""Test WGC direction setup."""

import pytest
from pytest import fixture, raises

from webgeocalc.direction import Direction
from webgeocalc.errors import CalculationInvalidAttr, CalculationRequiredAttr


def test_direction_position_with_shape():
    """Test direction position type with shape (for `AngularSeparation`)."""
    assert Direction(
        direction_type='POSITION',
        target='MARS',
        shape='POINT',
        observer='EARTH',
    ).payload == {
        'directionType': 'POSITION',
        'target': 'MARS',
        'shape': 'POINT',
        'observer': 'EARTH',
        'aberrationCorrection': 'NONE',
        'antiVectorFlag': False,
    }

def test_direction_position_without_shape():
    """Test direction position type without shape (for `PointingDirection`)."""
    assert Direction(
        direction_type='POSITION',
        target='MARS',
        observer='EARTH',
        aberration_correction='LT+S',
        anti_vector_flag='TRUE',  # Uppercase
    ).payload == {
        'directionType': 'POSITION',
        'target': 'MARS',
        'observer': 'EARTH',
        'aberrationCorrection': 'LT+S',
        'antiVectorFlag': True,
    }


def test_direction_position_errors():
    """Test direction position type errors """
    # Missing target
    with raises(CalculationRequiredAttr):
        _ = Direction(
            direction_type='POSITION',
            observer='EARTH',
        )

    # Missing observer
    with raises(CalculationRequiredAttr):
        _ = Direction(
            direction_type='POSITION',
            target='MARS',
            shape='POINT',
        )

    # Invalid shape
    with raises(CalculationInvalidAttr):
        _ = Direction(
            direction_type='POSITION',
            target='MARS',
            shape='WRONG',
            observer='EARTH',
        )

    # Invalid aberration correction
    with raises(CalculationInvalidAttr):
        _ = Direction(
            direction_type='POSITION',
            target='MARS',
            shape='SPHERE',
            observer='EARTH',
            aberration_correction='S',
        )

    # Invalid anti vector flag when shape is sphere
    with raises(CalculationInvalidAttr):
        _ = Direction(
            direction_type='POSITION',
            target='MARS',
            shape='SPHERE',
            observer='EARTH',
            anti_vector_flag=True,
        )


def test_direction_velocity():
    """Test direction velocity type."""
    assert Direction(
        direction_type='VELOCITY',
        target='MARS',
        reference_frame='itrf93',  # lowercase
        observer='EARTH',
        aberration_correction='XCN+S',
        anti_vector_flag='true',  # Lowercase
    ).payload == {
        'directionType': 'VELOCITY',
        'target': 'MARS',
        'referenceFrame': 'ITRF93',
        'observer': 'EARTH',
        'aberrationCorrection': 'XCN+S',
        'antiVectorFlag': True,
    }


def test_direction_position_errors():
    """Test direction position type errors """
    # Missing target
    with raises(CalculationRequiredAttr):
        _ = Direction(
            direction_type='VELOCITY',
            reference_frame='ITRF93',
            observer='EARTH',
        )

    # Missing reference frame
    with raises(CalculationRequiredAttr):
        _ = Direction(
            direction_type='VELOCITY',
            target='MARS',
            observer='EARTH',
        )

    # Missing observer
    with raises(CalculationRequiredAttr):
        _ = Direction(
            direction_type='VELOCITY',
            target='MARS',
            reference_frame='ITRF93',
        )


def test_direction_vector_inst_boresight():
    """Test direction vector for instrument boresight."""
    # Without observer (aberration correction NONE)
    assert Direction(
        direction_type='VECTOR',
        direction_vector_type='INSTRUMENT_BORESIGHT',
        direction_instrument='CASSINI_ISS_NAC',
    ).payload == {
        'directionType': 'VECTOR',
        'directionVectorType': 'INSTRUMENT_BORESIGHT',
        'directionInstrument': 'CASSINI_ISS_NAC',
        'aberrationCorrection': 'NONE',
        'antiVectorFlag': False,
    }

    # With explicit observer (aberration correction ≠ NONE)
    assert Direction(
        direction_type='VECTOR',
        observer='CASSINI',
        direction_vector_type='INSTRUMENT_BORESIGHT',
        direction_instrument='CASSINI_ISS_NAC',
        aberration_correction='CN'
    ).payload == {
        'directionType': 'VECTOR',
        'observer': 'CASSINI',
        'directionVectorType': 'INSTRUMENT_BORESIGHT',
        'directionInstrument': 'CASSINI_ISS_NAC',
        'aberrationCorrection': 'CN',
        'antiVectorFlag': False,
    }


def test_direction_vector_ref_frame_axis():
    """Test direction vector for reference fame axis."""
    assert Direction(
        direction_type='VECTOR',
        observer='EARTH',
        direction_vector_type='REFERENCE_FRAME_AXIS',
        direction_frame='IAU_EARTH',
        direction_frame_axis='X',
        aberration_correction='S',
        anti_vector_flag=True,
    ).payload == {
        'directionType': 'VECTOR',
        'observer': 'EARTH',
        'directionVectorType': 'REFERENCE_FRAME_AXIS',
        'directionFrame': 'IAU_EARTH',
        'directionFrameAxis': 'X',
        'aberrationCorrection': 'S',
        'antiVectorFlag': True,
    }


def test_direction_vector_in_instr_fov():
    """Test direction vector for in instrument FOV."""
    assert Direction(
        direction_type='VECTOR',
        direction_vector_type='VECTOR_IN_INSTRUMENT_FOV',
        direction_instrument='CASSINI_RPWS_EDIPOLE',
        direction_frame_axis='Z',
    ).payload == {
        'directionType': 'VECTOR',
        'directionVectorType': 'VECTOR_IN_INSTRUMENT_FOV',
        'directionInstrument': 'CASSINI_RPWS_EDIPOLE',
        'directionFrameAxis': 'Z',
        'aberrationCorrection': 'NONE',
        'antiVectorFlag': False,
    }


def test_direction_vector_errors():
    """Test direction vector errors."""
    # Missing direction_vector_type
    with raises(CalculationRequiredAttr):
        _ = Direction(
        direction_type='VECTOR',
    )

    # Missing observer with aberration correction NONE
    with raises(CalculationRequiredAttr):
        _ = Direction(
        direction_type='VECTOR',
        direction_vector_type='INSTRUMENT_BORESIGHT',
        direction_instrument='CASSINI_ISS_NAC',
        aberration_correction='CN',
    )

    #

## ---- Remove below FIXME -----


# @fixture
# def direction_vector_inst_boresight():
#     """Input vector direction."""
#     return {
#         "direction_type": "VECTOR",
#         "direction_vector_type": "INSTRUMENT_BORESIGHT",
#         "direction_instrument": "CASSINI_ISS_NAC",
#     }


# @fixture
# def direction_vector_inst_boresight_payload():
#     """Vector direction payload."""
#     return {
#         'aberrationCorrection': 'NONE',
#         'antiVectorFlag': False,
#         "directionType": "VECTOR",
#         "directionVectorType": "INSTRUMENT_BORESIGHT",
#         "directionInstrument": "CASSINI_ISS_NAC",
#     }


# @fixture
# def direction_vector_ref_frame_axis():
#     """Input vector direction."""
#     return {
#         "direction_type": "VECTOR",
#         "direction_vector_type": "REFERENCE_FRAME_AXIS",
#         "direction_frame": "CASSINI_RPWS_EDIPOLE",
#         "direction_frame_axis": "Z"
#     }


# @fixture
# def direction_vector_ref_frame_axis_payload():
#     """Vector direction payload."""
#     return {
#         'aberrationCorrection': 'NONE',
#         'antiVectorFlag': False,
#         "directionType": "VECTOR",
#         "directionVectorType": "REFERENCE_FRAME_AXIS",
#         "directionFrame": "CASSINI_RPWS_EDIPOLE",
#         "directionFrameAxis": "Z"
#     }


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


# @fixture
# def direction_velocity():
#     """Input velocity direction."""
#     return {
#         "directionType": "VELOCITY",
#         "target": "CASSINI",
#         "referenceFrame": "IAU_SATURN",
#         "observer": "SATURN"
#     }


# @fixture
# def direction_velocity_payload():
#     """Vector direction payload."""
#     return {
#         'aberrationCorrection': 'NONE',
#         'antiVectorFlag': False,
#         "directionType": "VELOCITY",
#         "target": "CASSINI",
#         "referenceFrame": "IAU_SATURN",
#         "observer": "SATURN"
#     }


# @fixture
# def direction_position():
#     """Input position direction."""
#     return {
#         "direction_type": "POSITION",
#         "target": "SUN",
#         "shape": "POINT",
#         "observer": "CASSINI"
#     }


# @fixture
# def direction_position_payload():
#     """Position direction payload."""
#     return {
#         'aberrationCorrection': 'NONE',
#         'antiVectorFlag': False,
#         "directionType": "POSITION",
#         "target": "SUN",
#         "shape": "POINT",
#         "observer": "CASSINI"
#     }


# @fixture
# def direction_position_anti_vector_flag_invalid():
#     """Input position direction."""
#     return {
#         "directionType": "POSITION",
#         "target": "SUN",
#         "shape": "POINT",
#         "observer": "CASSINI",
#         "antiVectorFlag": "Test"
#     }


@pytest.mark.parametrize("fixture_name", [
    # "direction_vector_inst_boresight",
    # "direction_vector_ref_frame_axis",
    "direction_vector_in_ref_frame_xyz",
    "direction_vector_in_ref_frame_radec",
    "direction_vector_in_ref_frame_azel",
    # "direction_velocity",
    # "direction_position",
])
def test_direction_vector_in_ref_frame(request, fixture_name):
    """Test direction payload."""
    params = request.getfixturevalue(fixture_name)
    payload = request.getfixturevalue(fixture_name + '_payload')
    assert Direction(**params).payload == payload


# def test_direction_position_anti_vector_flag_invalid_error(
#     direction_position_anti_vector_flag_invalid
# ):
#     """Test anti-vector flag error."""
#     with raises(CalculationInvalidAttr):
#         Direction(**direction_position_anti_vector_flag_invalid)
