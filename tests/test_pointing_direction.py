"""Test WGC pointing direction calculation."""

from pytest import raises

from webgeocalc import PointingDirection
from webgeocalc.direction import Direction
from webgeocalc.errors import CalculationInvalidAttr, CalculationRequiredAttr


def test_pointing_direction_payload():
    """Test pointing direction payload."""
    assert PointingDirection(
        kernels=5,
        times='2012-10-19T08:24:00.000',
        direction={
            'direction_type': 'VECTOR',
            'observer': 'CASSINI',
            'direction_vector_type': 'INSTRUMENT_FOV_BOUNDARY_VECTORS',
            'direction_instrument': 'CASSINI_ISS_NAC',
            'aberration_correction': 'CN',
        },
        reference_frame='DSS-13_TOPO',
        coordinate_representation='AZ_EL',
        azccw_flag='FALSE',
        elplsz_flag='false',
    ).payload == {
        "kernels": [{"type": "KERNEL_SET", "id": 5}],
        "timeSystem": "UTC",
        "timeFormat": "CALENDAR",
        "times": ['2012-10-19T08:24:00.000'],
        "direction": {
            "directionType": "VECTOR",
            "observer": "CASSINI",
            "directionVectorType": "INSTRUMENT_FOV_BOUNDARY_VECTORS",
            "directionInstrument": "CASSINI_ISS_NAC",
            "aberrationCorrection": "CN",
            "antiVectorFlag": False,
        },
        "referenceFrame": "DSS-13_TOPO",
        "calculationType": "POINTING_DIRECTION",
        "vectorMagnitude": "UNIT",
        "coordinateRepresentation": "AZ_EL",
        "azccwFlag": False,
        "elplszFlag": False,
    }


def test_pointing_direction_errors():
    """Test pointing direction errors."""
    direction = Direction(
        direction_type='VECTOR',
        direction_vector_type='INSTRUMENT_BORESIGHT',
        direction_instrument='CASSINI_ISS_NAC',
    )

    # Invalid `vector_magnitude`
    with raises(CalculationInvalidAttr):
        PointingDirection(
            kernels=5,
            times='2012-10-19T08:24:00.000',
            direction=direction,
            reference_frame='J2000',
            vector_magnitude='WRONG',
        )

    # Invalid `coordinate_representation` (PLANETODETIC is excluded)
    with raises(CalculationInvalidAttr):
        PointingDirection(
            kernels=5,
            times='2012-10-19T08:24:00.000',
            direction=direction,
            reference_frame='IAU_EARTH',
            coordinate_representation='PLANETODETIC',
        )

    # Missing `azccw_flag` or `elplsz_flag` with `coordinate_representation='AZ_EL'`
    with raises(CalculationRequiredAttr):
        PointingDirection(
            kernels=5,
            times='2012-10-19T08:24:00.000',
            direction=direction,
            reference_frame='DSS-13_TOPO',
            coordinate_representation='AZ_EL',
        )
