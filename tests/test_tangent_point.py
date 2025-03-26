"""Test WGC tangent point calculation."""

from pytest import raises

from webgeocalc import TangentPoint
from webgeocalc.errors import CalculationInvalidAttr, CalculationRequiredAttr


def test_pointing_direction_payload():
    """Test tangent point payload."""
    assert TangentPoint(
        kernels=5,
        times='2012-11-30T14:02:00',
        target='ENCELADUS',
        target_frame='IAU_ENCELADUS',
        observer='CASSINI',
        direction_vector_type='VECTOR_IN_REFERENCE_FRAME',
        direction_frame='J2000',
        direction_vector_az=210,
        direction_vector_el=10,
        azccw_flag='True',
        elplsz_flag=False,
        aberration_correction='CN+S',
        correction_locus='TANGENT_POINT',
    ) == {
        "kernels": [{"type": "KERNEL_SET", "id": 5}],
        "timeSystem": "UTC",
        "timeFormat": "CALENDAR",
        "times": ['2012-11-30T14:02:00'],
        "target": "ENCELADUS",
        "targetFrame": "IAU_ENCELADUS",
        "observer": "CASSINI",
        "directionVectorType": "VECTOR_IN_REFERENCE_FRAME",
        "directionFrame": "J2000",
        "directionVectorAz": 210,
        "directionVectorEl": 10,
        "azccwFlag": True,
        "elplszFlag": False,
        "correctionLocus": "TANGENT_POINT",
        "calculationType": "TANGENT_POINT",
        "computationMethod": "ELLIPSOID",
        "vectorAbCorr": "NONE",  # Appended only for `VECTOR_IN_REFERENCE_FRAME`
        "aberrationCorrection": "CN+S",
        "coordinateRepresentation": "RECTANGULAR",
    }

    # With direction to object
    assert TangentPoint(
        kernels=5,
        times='2012-11-30T14:02:00',
        target='ENCELADUS',
        target_frame='IAU_ENCELADUS',
        observer='CASSINI',
        direction_vector_type='DIRECTION_TO_OBJECT',
        direction_object='SATURN',
        aberration_correction='NONE',
        correction_locus='SURFACE_POINT',
        coordinate_representation='SPHERICAL',
    ) == {
        "kernels": [{"type": "KERNEL_SET", "id": 5}],
        "timeSystem": "UTC",
        "timeFormat": "CALENDAR",
        "times": ['2012-11-30T14:02:00'],
        "target": "ENCELADUS",
        "targetFrame": "IAU_ENCELADUS",
        "observer": "CASSINI",
        "directionVectorType": "DIRECTION_TO_OBJECT",
        "directionObject": "SATURN",
        "correctionLocus": "SURFACE_POINT",
        "calculationType": "TANGENT_POINT",
        "computationMethod": "ELLIPSOID",
        "aberrationCorrection": "NONE",
        "coordinateRepresentation": "SPHERICAL",
    }


def test_tangent_point_errors():
    """Test tangent point errors."""
    # Requires `correction_locus` for aberration correction not None
    with raises(CalculationRequiredAttr, match='correction_locus'):
        TangentPoint(
            kernels=5,
            times='2012-11-30T14:02:00',
            target='ENCELADUS',
            target_frame='IAU_ENCELADUS',
            observer='CASSINI',
            direction_vector_type='INSTRUMENT_BORESIGHT',
        )

    # Invalid `coordinate_representation` (PLANETODETIC is excluded)
    with raises(CalculationInvalidAttr, match='coordinate_representation'):
        TangentPoint(
            kernels=5,
            times='2012-11-30T14:02:00',
            target='ENCELADUS',
            target_frame='IAU_ENCELADUS',
            observer='CASSINI',
            direction_vector_type='INSTRUMENT_BORESIGHT',
            aberration_correction='NONE',
            coordinate_representation='WRONG',
        )
