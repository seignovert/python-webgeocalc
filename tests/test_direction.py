"""Test WGC direction setup."""

import pytest
from pytest import fixture, raises

from webgeocalc.calculation import _Direction
from webgeocalc.errors import CalculationInvalidAttr


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


@pytest.mark.parametrize("fixture_name", [
    "direction_vector_inst_boresight",
    "direction_vector_ref_frame_axis",
    "direction_vector_in_ref_frame_xyz",
    "direction_vector_in_ref_frame_radec",
    "direction_vector_in_ref_frame_azel",
    "direction_velocity",
    "direction_position",
])
def test_direction_vector_in_ref_frame(request, fixture_name):
    """Test direction payload."""
    params = request.getfixturevalue(fixture_name)
    payload = request.getfixturevalue(fixture_name + '_payload')
    assert _Direction(**params).payload == payload


def test_direction_position_anti_vector_flag_invalid_error(
    direction_position_anti_vector_flag_invalid
):
    """Test anti-vector flag error."""
    with raises(CalculationInvalidAttr):
        _Direction(**direction_position_anti_vector_flag_invalid)
