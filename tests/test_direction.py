"""Test WGC direction setup."""

import re

from pytest import raises

from webgeocalc.direction import Direction
from webgeocalc.errors import (CalculationIncompatibleAttr, CalculationInvalidAttr,
                               CalculationRequiredAttr, CalculationUndefinedAttr)


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
    """Test direction position type errors."""
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
            aberration_correction='S',  # only for direction VECTOR
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


def test_direction_velocity_errors():
    """Test direction velocity type errors."""
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


def test_direction_vector_instrument_boresight():
    """Test direction vector with instrument boresight."""
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


def test_direction_vector_frame_axis():
    """Test direction vector with fame axis."""
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


def test_direction_vector_in_instrument_fov_xyz():
    """Test direction vector with in instrument FOV (X/Y/Z)."""
    assert Direction(
        direction_type='VECTOR',
        direction_vector_type='VECTOR_IN_INSTRUMENT_FOV',
        direction_instrument='CASSINI_ISS_NAC',
        direction_vector_x=0,
        direction_vector_y=0,
        direction_vector_z=1,
    ).payload == {
        'directionType': 'VECTOR',
        'directionVectorType': 'VECTOR_IN_INSTRUMENT_FOV',
        'directionInstrument': 'CASSINI_ISS_NAC',
        'directionVectorX': 0,
        'directionVectorY': 0,
        'directionVectorZ': 1,
        'aberrationCorrection': 'NONE',
        'antiVectorFlag': False,
    }


def test_direction_vector_in_reference_frame_radec():
    """Test direction vector with in reference fame (RA/DEC)."""
    assert Direction(
        direction_type='VECTOR',
        direction_vector_type='VECTOR_IN_REFERENCE_FRAME',
        direction_frame='J2000',
        direction_vector_ra=0,
        direction_vector_dec=45,
    ).payload == {
        'directionType': 'VECTOR',
        'directionVectorType': 'VECTOR_IN_REFERENCE_FRAME',
        'directionFrame': 'J2000',
        'directionVectorRA': 0,
        'directionVectorDec': 45,
        'aberrationCorrection': 'NONE',
        'antiVectorFlag': False,
    }


def test_direction_vector_in_reference_frame_azel():
    """Test direction vector with in reference fame (AZ/EL)."""
    assert Direction(
        direction_type='VECTOR',
        direction_vector_type='VECTOR_IN_REFERENCE_FRAME',
        direction_frame='DSS-13_TOPO',
        direction_vector_az=5,
        direction_vector_el=15,
        azccw_flag=True,
        elplsz_flag='True',
    ).payload == {
        'directionType': 'VECTOR',
        'directionVectorType': 'VECTOR_IN_REFERENCE_FRAME',
        'directionFrame': 'DSS-13_TOPO',
        'directionVectorAz': 5,
        'directionVectorEl': 15,
        "azccwFlag": True,
        "elplszFlag": True,
        'aberrationCorrection': 'NONE',
        'antiVectorFlag': False,
    }


def test_direction_vector_instrument_fov_boundary_vectors():
    """Test direction vector with instrument FOV boundary vectors."""
    assert Direction(
        direction_type='VECTOR',
        observer='CASSINI',
        direction_vector_type='INSTRUMENT_FOV_BOUNDARY_VECTORS',
        direction_instrument='CASSINI_ISS_NAC',
        aberration_correction='CN',
    ).payload == {
        'directionType': 'VECTOR',
        'observer': 'CASSINI',
        'directionVectorType': 'INSTRUMENT_FOV_BOUNDARY_VECTORS',
        'directionInstrument': 'CASSINI_ISS_NAC',
        'aberrationCorrection': 'CN',
        'antiVectorFlag': False,
    }


def test_direction_vector_requirements_errors():
    """Test direction vector requirements errors."""
    # Missing direction_vector_type
    with raises(CalculationRequiredAttr):
        _ = Direction(
            direction_type='VECTOR',
        )

    # Missing direction_instrument (with INSTRUMENT_BORESIGHT)
    with raises(CalculationRequiredAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='INSTRUMENT_BORESIGHT',
        )

    # Missing direction_instrument (with VECTOR_IN_INSTRUMENT_FOV)
    with raises(CalculationRequiredAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='VECTOR_IN_INSTRUMENT_FOV',
        )

    # Missing direction_instrument (with INSTRUMENT_FOV_BOUNDARY_VECTORS)
    with raises(CalculationRequiredAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='INSTRUMENT_FOV_BOUNDARY_VECTORS',
        )

    # Missing direction_frame (with REFERENCE_FRAME_AXIS)
    with raises(CalculationRequiredAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='REFERENCE_FRAME_AXIS',
        )

    # Missing direction_frame (with VECTOR_IN_REFERENCE_FRAME)
    with raises(CalculationRequiredAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='VECTOR_IN_REFERENCE_FRAME',
        )

    # Missing direction_frame_axis (with REFERENCE_FRAME_AXIS)
    with raises(CalculationRequiredAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='REFERENCE_FRAME_AXIS',
            direction_frame='IAU_EARTH',
        )


def test_direction_vector_coordinates_errors():
    """Test direction vector coordinates errors."""
    err = re.escape(
        "Attribute 'direction_vector_type' is set "
        "to 'VECTOR_IN_INSTRUMENT_FOV' "
        "but 'direction_vector_x/y/z' or "
        "'direction_vector_ra/dec' or "
        "'direction_vector_az/el' attribute is undefined."
    )
    # Missing direction_vector_x
    with raises(CalculationUndefinedAttr, match=err):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='VECTOR_IN_INSTRUMENT_FOV',
            direction_instrument='CASSINI_ISS_NAC',
            direction_vector_y=0,
            direction_vector_z=1,
        )

    # Missing direction_vector_y
    with raises(CalculationUndefinedAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='VECTOR_IN_INSTRUMENT_FOV',
            direction_instrument='CASSINI_ISS_NAC',
            direction_vector_x=0,
            direction_vector_z=1,
        )

    # Missing direction_vector_z
    with raises(CalculationUndefinedAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='VECTOR_IN_INSTRUMENT_FOV',
            direction_instrument='CASSINI_ISS_NAC',
            direction_vector_x=0,
            direction_vector_y=0,
        )

    # Missing direction_vector_ra
    with raises(CalculationUndefinedAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='VECTOR_IN_REFERENCE_FRAME',
            direction_frame='J2000',
            direction_vector_dec=45,
        )

    # Missing direction_vector_dec
    with raises(CalculationUndefinedAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='VECTOR_IN_REFERENCE_FRAME',
            direction_frame='J2000',
            direction_vector_ra=0,
        )

    # Missing direction_vector_az
    with raises(CalculationUndefinedAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='VECTOR_IN_REFERENCE_FRAME',
            direction_frame='DSS-13_TOPO',
            direction_vector_el=15,
            azccw_flag=True,
            elplsz_flag=True,
        )

    # Missing direction_vector_el
    with raises(CalculationUndefinedAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='VECTOR_IN_REFERENCE_FRAME',
            direction_frame='DSS-13_TOPO',
            direction_vector_az=5,
            azccw_flag=True,
            elplsz_flag=True,
        )

    # Missing azccw_flag
    with raises(CalculationRequiredAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='VECTOR_IN_REFERENCE_FRAME',
            direction_frame='DSS-13_TOPO',
            direction_vector_az=5,
            direction_vector_el=15,
            elplsz_flag=True,
        )

    # Missing elplsz_flag
    with raises(CalculationRequiredAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='VECTOR_IN_REFERENCE_FRAME',
            direction_frame='DSS-13_TOPO',
            direction_vector_az=5,
            direction_vector_el=15,
            azccw_flag=True,
        )

    # Missing direction_vector_az with azccw_flag
    with raises(CalculationUndefinedAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='INSTRUMENT_BORESIGHT',
            direction_instrument='CASSINI_ISS_NAC',
            azccw_flag=True,
        )

    # Missing direction_vector_el with elplsz_flag
    with raises(CalculationUndefinedAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='INSTRUMENT_BORESIGHT',
            direction_instrument='CASSINI_ISS_NAC',
            elplsz_flag=True,
        )


def test_direction_vector_abcorr_errors():
    """Test direction vector aberration correction errors."""
    # Missing observer with aberration correction NONE
    with raises(CalculationRequiredAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='INSTRUMENT_BORESIGHT',
            direction_instrument='CASSINI_ISS_NAC',
            aberration_correction='CN',
        )

    # Invalid with aberration correction with VECTOR
    with raises(CalculationInvalidAttr):
        _ = Direction(
            direction_type='VECTOR',
            observer='CASSINI',
            direction_vector_type='INSTRUMENT_BORESIGHT',
            direction_instrument='CASSINI_ISS_NAC',
            aberration_correction='CN+S',  # +S invalid for direction VECTOR
        )


def test_direction_vector_invalid_errors():
    """Test direction vector invalid errors."""
    # Invalid direction_vector_type
    with raises(CalculationInvalidAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='WRONG',
        )

    # Invalid direction_frame_axis
    with raises(CalculationInvalidAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='REFERENCE_FRAME_AXIS',
            direction_frame='IAU_EARTH',
            direction_frame_axis='W',
        )

    # Invalid azccw_flag
    with raises(CalculationInvalidAttr):
        assert Direction(
            direction_type='VECTOR',
            direction_vector_type='VECTOR_IN_REFERENCE_FRAME',
            direction_frame='DSS-13_TOPO',
            direction_vector_az=5,
            direction_vector_el=15,
            azccw_flag='WRONG',
            elplsz_flag=True,
        )

    # Invalid elplsz_flag
    with raises(CalculationInvalidAttr):
        assert Direction(
            direction_type='VECTOR',
            direction_vector_type='VECTOR_IN_REFERENCE_FRAME',
            direction_frame='DSS-13_TOPO',
            direction_vector_az=5,
            direction_vector_el=15,
            azccw_flag='TRUE',
            elplsz_flag='WRONG',
        )


def test_direction_vector_incompatible_errors():
    """Test direction vector incompatibility errors."""
    # Incompatible direction_instrument (with REFERENCE_FRAME_AXIS)
    with raises(CalculationIncompatibleAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='REFERENCE_FRAME_AXIS',
            direction_frame='IAU_EARTH',
            direction_frame_axis='X',
            direction_instrument='INCOMPATIBLE',
        )

    # Incompatible direction_instrument (with VECTOR_IN_REFERENCE_FRAME)
    with raises(CalculationIncompatibleAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='VECTOR_IN_REFERENCE_FRAME',
            direction_frame='J2000',
            direction_vector_ra=0,
            direction_vector_dec=45,
            direction_instrument='INCOMPATIBLE',
        )

    # Incompatible direction_frame (with INSTRUMENT_BORESIGHT)
    with raises(CalculationIncompatibleAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='INSTRUMENT_BORESIGHT',
            direction_instrument='CASSINI_ISS_NAC',
            direction_frame='INCOMPATIBLE',
        )

    # Incompatible direction_frame (with VECTOR_IN_INSTRUMENT_FOV)
    with raises(CalculationIncompatibleAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='VECTOR_IN_INSTRUMENT_FOV',
            direction_instrument='CASSINI_ISS_NAC',
            direction_frame='INCOMPATIBLE',
            direction_vector_x=0,
            direction_vector_y=0,
            direction_vector_z=1,
        )

    # Incompatible direction_frame (with INSTRUMENT_FOV_BOUNDARY_VECTORS)
    with raises(CalculationIncompatibleAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='INSTRUMENT_FOV_BOUNDARY_VECTORS',
            direction_instrument='CASSINI_ISS_NAC',
            direction_frame='INCOMPATIBLE',
        )

    # Incompatible direction_frame_axis (without REFERENCE_FRAME_AXIS)
    with raises(CalculationIncompatibleAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='INSTRUMENT_BORESIGHT',
            direction_instrument='CASSINI_ISS_NAC',
            direction_frame_axis='X',
        )

    # Incompatible direction_vector_x|y|z|ra|dec|az|el
    # (without VECTOR_IN_INSTRUMENT_FOV or VECTOR_IN_REFERENCE_FRAME)
    with raises(CalculationIncompatibleAttr):
        _ = Direction(
            direction_type='VECTOR',
            direction_vector_type='INSTRUMENT_BORESIGHT',
            direction_instrument='CASSINI_ISS_NAC',
            direction_vector_x=0,
        )
