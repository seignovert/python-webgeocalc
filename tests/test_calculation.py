"""Test WGC calculation setup."""

from pytest import fixture, raises

from webgeocalc import Calculation
from webgeocalc.api import API
from webgeocalc.calculation import APIs
from webgeocalc.errors import (CalculationConflictAttr,
                               CalculationIncompatibleAttr,
                               CalculationInvalidAttr, CalculationRequiredAttr,
                               CalculationUndefinedAttr)
from webgeocalc.vars import ESA_URL, JPL_URL


@fixture
def kernels():
    """Input Solar System kernels set."""
    return 1


@fixture
def calc():
    """Input calculation type name."""
    return 'STATE_VECTOR'


@fixture
def time():
    """Input time."""
    return '2012-10-19T08:24:00.000'


@fixture
def path():
    """Input kernel path url."""
    return 'https://path.to.server/kernel'


@fixture
def params(calc, path, time):
    """Input parameters dict."""
    return {
        'calculation_type': calc,
        'kernel_paths': path,
        'times': time,
    }


@fixture
def start():
    """Input start time."""
    return '2000-01-01'


@fixture
def end():
    """Input end time."""
    return '2000-01-02'


@fixture
def interval(start, end):
    """Input interval dict."""
    return {"startTime": start, "endTime": end}


def test_calculation_api(params):
    """Test calculation API URL."""
    api = Calculation(**params).api
    assert api.url == JPL_URL

    api = Calculation(api='ESA', **params).api
    assert api.url == ESA_URL


def test_calculation_apis_cache(params):
    """Test calculation APIs caching."""
    assert len(APIs) == 3
    assert str(APIs['JPL']) == JPL_URL
    assert str(APIs['ESA']) == ESA_URL
    assert str(APIs['']) == API.url

    # Add 3rd party API
    assert 'HTTPS://WGC.OBSPM.FR/WEBGEOCALC/API' not in APIs

    api = Calculation(api='https://wgc.obspm.fr/webgeocalc/api', **params).api
    assert api.url == 'https://wgc.obspm.fr/webgeocalc/api'

    # Check API caching
    assert len(APIs) == 4
    assert 'HTTPS://WGC.OBSPM.FR/WEBGEOCALC/API' in APIs
    assert APIs['HTTPS://WGC.OBSPM.FR/WEBGEOCALC/API'].url == \
        'https://wgc.obspm.fr/webgeocalc/api'

    api = Calculation(api='https://wgc.obspm.fr/webgeocalc/api', **params).api
    assert api.url == 'https://wgc.obspm.fr/webgeocalc/api'
    assert len(APIs) == 4

    # Input directly a `Api` object
    api = Calculation(api=api, **params).api
    assert api.url == 'https://wgc.obspm.fr/webgeocalc/api'
    assert len(APIs) == 4


def test_calculation_required_err(calc, kernels):
    """Test error if calculation has missing required attributes."""
    with raises(CalculationRequiredAttr):
        Calculation()  # 'calculation_type' missing

    with raises(CalculationRequiredAttr):
        Calculation(calculation_type=calc)  # 'kernels/kernel_paths' missing

    with raises(CalculationRequiredAttr):
        Calculation(calculation_type=calc, kernels=kernels)  # 'times' missing


def test_calculation_calc_err(params):
    """Test error if calculation type is invalid."""
    params['calculation_type'] = 'WRONG'
    with raises(CalculationInvalidAttr):
        Calculation(**params)


def test_calculation_time_system_err(params):
    """Test error if time system is invalid."""
    params['time_system'] = 'WRONG'
    with raises(CalculationInvalidAttr):
        Calculation(**params)


def test_calculation_missing_sclk_id(params):
    """Test error if sclk_id is missing."""
    params['time_system'] = 'SPACECRAFT_CLOCK'
    with raises(CalculationUndefinedAttr):
        Calculation(**params)


def test_calculation_time_format_error(params):
    """Test error if time format is invalid."""
    params['time_format'] = 'WRONG'
    with raises(CalculationInvalidAttr):
        Calculation(**params)


def test_calculation_time_system_conflict(params):
    """Test error when time system and time format are incompatible."""
    params['time_system'] = 'SPACECRAFT_CLOCK'
    params['sclk_id'] = 1
    with raises(CalculationIncompatibleAttr):
        Calculation(**params)


def test_calculation_time_format_conflict(params):
    """Test error when time format and time system are incompatible."""
    params['time_format'] = 'SPACECRAFT_CLOCK_STRING'
    with raises(CalculationIncompatibleAttr):
        Calculation(**params)


def test_calculation_sclk_id_conflict(params):
    """Test error when sclk id system and time system are incompatible."""
    params['sclk_id'] = 1
    with raises(CalculationIncompatibleAttr):
        Calculation(**params)


def test_calculation_intervals(params, start, end, interval):
    """Test calculation interval inputs."""
    del params['times']
    params['time_step'] = 1
    params['time_step_units'] = 'DAYS'

    params['intervals'] = [start, end]
    assert Calculation(**params).payload['intervals'] == [interval]

    params['intervals'] = {"startTime": start, "endTime": end}
    assert Calculation(**params).payload['intervals'] == [interval]

    params['intervals'] = [interval]
    assert Calculation(**params).payload['intervals'] == [interval]

    params['intervals'] = [interval, interval]
    assert Calculation(**params).payload['intervals'] == [interval, interval]

    params['intervals'] = [interval, interval, interval]
    assert Calculation(**params).payload['intervals'] == [interval, interval, interval]


def test_calculation_intervals_errors(params, start, end, interval):
    """Test errors if intervals input are incorrect."""
    params['intervals'] = interval

    with raises(CalculationConflictAttr):
        Calculation(**params)  # 'times' and 'intervals' conflict

    del params['times']

    with raises(CalculationUndefinedAttr):
        Calculation(**params)  # 'time_step' missing

    params['time_step'] = 1
    with raises(CalculationUndefinedAttr):
        Calculation(**params)  # 'time_step_units' missing

    params['time_step_units'] = 'DAYS'

    params['intervals'] = {"startTime": start, "wrongEndTime": end}
    with raises(CalculationInvalidAttr):
        Calculation(**params)

    params['intervals'] = []
    with raises(CalculationInvalidAttr):
        Calculation(**params)

    params['intervals'] = [start]
    with raises(CalculationInvalidAttr):
        Calculation(**params)

    params['intervals'] = [start, interval]
    with raises(CalculationInvalidAttr):
        Calculation(**params)

    params['intervals'] = [start, end, end]
    with raises(CalculationInvalidAttr):
        Calculation(**params)


def test_calculation_time_step_conflict(params):
    """Test error when time step and times are incompatible."""
    params['time_step'] = 1
    with raises(CalculationConflictAttr):
        Calculation(**params)


def test_calculation_time_step_units_errors(params, interval):
    """Test errors if time step units are invalid."""
    params['time_step_units'] = 'DAYS'
    with raises(CalculationConflictAttr):
        Calculation(**params)  # Conflict with 'times'

    del params['times']
    params['intervals'] = interval

    with raises(CalculationUndefinedAttr):
        Calculation(**params)  # 'time_step' missing

    params['time_step'] = 1
    params['time_step_units'] = 'WRONG_UNITS'
    with raises(CalculationInvalidAttr):
        Calculation(**params)


def test_calculation_aberration_correction_error(params):
    """Test error if aberration correction is invalid."""
    with raises(CalculationInvalidAttr):
        Calculation(aberration_correction='WRONG', **params)


def test_calculation_vector_ab_corr_error(params):
    """Test type of aberration correction errors."""
    # Missing `direction_vector_type`
    with raises(CalculationUndefinedAttr, match='direction_vector_type'):
        Calculation(vector_ab_corr='NONE', **params)

    # Invalid `direction_vector_type` (not `VECTOR_IN_REFERENCE_FRAME`)
    with raises(CalculationIncompatibleAttr, match='VECTOR_IN_REFERENCE_FRAME'):
        Calculation(direction_vector_type='INSTRUMENT_BORESIGHT',
                    direction_instrument='CASSINI_ISS_NAC',
                    vector_ab_corr='NONE', **params)

    # Invalid attribute
    with raises(CalculationInvalidAttr):
        Calculation(direction_vector_type='VECTOR_IN_REFERENCE_FRAME',
                    direction_frame='J2000',
                    direction_vector_ra=210,
                    direction_vector_dec=-10,
                    vector_ab_corr='WRONG', **params)


def test_calculation_correction_locus_error(params):
    """Test aberration correction locus errors."""
    with raises(CalculationInvalidAttr):
        Calculation(correction_locus='WRONG', **params)


def test_calculation_spec_type_error(params):
    """Test angular separation computation type errors."""
    with raises(CalculationInvalidAttr):
        Calculation(spec_type='WRONG', **params)


def test_calculation_vector_magnitude_error(params):
    """Test vector magnitude errors."""
    with raises(CalculationInvalidAttr):
        Calculation(vector_magnitude='WRONG', **params)


def test_calculation_computation_method_error(params):
    """Test computation method (for TANGENT POINT) errors."""
    with raises(CalculationInvalidAttr):
        Calculation(computation_method='WRONG', **params)


def test_calculation_state_representation_error(params):
    """Test error if state representation is invalid."""
    with raises(CalculationInvalidAttr):
        Calculation(state_representation='WRONG', **params)


def test_calculation_time_location_error(params):
    """Test frame for the input times errors."""
    with raises(CalculationInvalidAttr):
        Calculation(time_location='WRONG', **params)


def test_calculation_orientation_representation_error(params):
    """Test representation of the result transformation errors."""
    with raises(CalculationInvalidAttr):
        Calculation(orientation_representation='WRONG', **params)


def test_calculation_shape_error(params):
    """Test error if shape 1-2 is invalid."""
    with raises(CalculationInvalidAttr):
        Calculation(shape_1='WRONG', **params)

    with raises(CalculationInvalidAttr):
        Calculation(shape_2='WRONG', **params)


def test_calculation_axis_error(params):
    """Test error if axis inputs are invalid."""
    with raises(CalculationUndefinedAttr):
        Calculation(axis_1='X', **params)  # Missing `orientation_representation`

    with raises(CalculationIncompatibleAttr):
        # Wrong `orientation_representation` with `axis`
        Calculation(orientation_representation='SPICE_QUATERNION', axis_1='X', **params)


def test_calculation_angular_units_error(params):
    """Test errors if angular units are invalid."""
    with raises(CalculationInvalidAttr):
        Calculation(angular_units='WRONG', **params)

    with raises(CalculationUndefinedAttr):
        Calculation(angular_units='deg', **params)  # Missing `orientation_representation`

    with raises(CalculationIncompatibleAttr):
        # Wrong `orientation_representation` with `angular_units`
        Calculation(orientation_representation='SPICE_QUATERNION',
                    angular_units='deg', **params)


def test_calculation_angular_velocity_representation_error(params):
    """Test angular velocity representation errors."""
    with raises(CalculationInvalidAttr):
        Calculation(angular_velocity_representation='WRONG', **params)


def test_calculation_angular_velocity_units_error(params):
    """Test errors with angular velocity units."""
    with raises(CalculationInvalidAttr):
        Calculation(angular_velocity_units='WRONG', **params)

    with raises(CalculationUndefinedAttr):
        # Missing `angular_velocity_representation`
        Calculation(angular_velocity_units='deg/s', **params)

    with raises(CalculationIncompatibleAttr):
        # Wrong `angular_velocity_representation` with `angular_velocity_units`
        Calculation(angular_velocity_representation='NOT_INCLUDED',
                    angular_velocity_units='deg/s', **params)


def test_calculation_coordinate_representation_error(params):
    """Test Coordinate representation errors."""
    with raises(CalculationInvalidAttr):
        Calculation(coordinate_representation='WRONG', **params)


def test_calculation_sub_point_type_error(params):
    """Test sub-observer point errors."""
    with raises(CalculationInvalidAttr):
        Calculation(sub_point_type='WRONG', **params)


def test_calculation_direction_vector_type_error(params):
    """Test error if direction vector type is invalid."""
    with raises(CalculationInvalidAttr):
        Calculation(direction_vector_type='WRONG', **params)

    # Missing `direction_object` attribute
    with raises(CalculationRequiredAttr, match='direction_object'):
        Calculation(direction_vector_type='DIRECTION_TO_OBJECT', **params)

    # DIRECTION_TO_OBJECT can only be used with `TANGENT_POINT` calculation
    with raises(CalculationIncompatibleAttr, match='direction_vector_type'):
        Calculation(
            direction_vector_type='DIRECTION_TO_OBJECT',
            direction_object='ANY',
            **params
        )


def test_calculation_direction_object_error(params):
    """Test errors when direction object is invalid."""
    # Missing `direction_vector_type`
    with raises(CalculationUndefinedAttr, match='direction_vector_type'):
        Calculation(direction_object='CASSINI_ISS_NAC', **params)

    # Invalid `direction_vector_type` (only `DIRECTION_TO_OBJECT`)
    with raises(CalculationIncompatibleAttr, match='direction_object'):
        Calculation(direction_vector_type='INSTRUMENT_BORESIGHT',
                    direction_instrument='CASSINI_ISS_NAC',
                    direction_object='ANY', **params)


def test_calculation_direction_instrument_error(params):
    """Test errors when direction instrument is invalid."""
    with raises(CalculationUndefinedAttr):
        # Missing `direction_vector_type`
        Calculation(direction_instrument='CASSINI_ISS_NAC', **params)

    with raises(CalculationIncompatibleAttr):
        Calculation(direction_instrument='CASSINI_ISS_NAC',
                    direction_vector_type='VECTOR_IN_REFERENCE_FRAME',
                    direction_frame='CASSINI_ISS_NAC', **params)


def test_calculation_direction_frame_error(params):
    """Test errors when direction frame is invalid."""
    with raises(CalculationUndefinedAttr):
        # Missing 'direction_vector_type'
        Calculation(direction_frame='CASSINI_ISS_NAC', **params)

    with raises(CalculationIncompatibleAttr):
        # Wrong 'direction_vector_type'
        Calculation(direction_frame='CASSINI_ISS_NAC',
                    direction_vector_type='INSTRUMENT_BORESIGHT', **params)


def test_calculation_direction_frame_axis_error(params):
    """Test errors when direction frame axis is invalid."""
    with raises(CalculationUndefinedAttr):
        # Missing 'direction_frame'
        Calculation(direction_frame_axis='Z', **params)

    with raises(CalculationIncompatibleAttr):
        # Wrong 'direction_vector_type'
        Calculation(direction_frame_axis='Z',
                    direction_vector_type='INSTRUMENT_BORESIGHT', **params)

    with raises(CalculationInvalidAttr):
        # Wrong 'direction_frame_axis'
        Calculation(direction_frame_axis='WRONG',
                    direction_vector_type='REFERENCE_FRAME_AXIS', **params)


def test_calculation_direction_vector_error(params):
    """Test errors when direction vector is invalid."""
    with raises(CalculationUndefinedAttr):
        # Missing 'direction_vector_type'
        Calculation(direction_vector_x=0, **params)

    with raises(CalculationIncompatibleAttr):
        # Wrong 'direction_vector_type'
        Calculation(direction_vector_x=0,
                    direction_vector_type='INSTRUMENT_BORESIGHT', **params)


def test_calculation_direction_vector_az_el_error(params):
    """Test errors when direction vector azimuth/elevation are invalid."""
    with raises(CalculationRequiredAttr, match='azccw_flag'):
        Calculation(direction_vector_az='WRONG', **params)

    with raises(CalculationRequiredAttr, match='elplsz_flag'):
        Calculation(direction_vector_el='WRONG', **params)


def test_calculation_azccw_elplsz_flag_error(params):
    """Test errors when azimuth or elevation flags are invalid."""
    with raises(CalculationInvalidAttr):
        Calculation(azccw_flag='WRONG', **params)

    with raises(CalculationInvalidAttr):
        Calculation(elplsz_flag='WRONG', **params)


def test_calculation_output_duration_units_error(params):
    """Test errors when output duration units is invalid."""
    with raises(CalculationInvalidAttr):
        Calculation(output_duration_units='WRONG', **params)


def test_calculation_interval_adjustment_errors(params):
    """Test errors when interval parameters are invalid."""
    with raises(CalculationInvalidAttr):
        Calculation(interval_adjustment='WRONG', **params)

    with raises(CalculationInvalidAttr):
        Calculation(interval_adjustment_units='WRONG', **params)

    with raises(CalculationInvalidAttr):
        Calculation(interval_filtering='WRONG', **params)

    with raises(CalculationInvalidAttr):
        Calculation(interval_filtering='WRONG', **params)

    with raises(CalculationInvalidAttr):
        Calculation(interval_filtering_threshold_units='WRONG', **params)


def test_calculation_coordinate_errors(params):
    """Test errors when coordinate are invalid."""
    with raises(CalculationInvalidAttr):
        Calculation(coordinate_system='WRONG', **params)

    with raises(CalculationInvalidAttr):
        Calculation(coordinate='WRONG', **params)

    with raises(CalculationInvalidAttr):
        Calculation(relational_condition='WRONG', **params)


def test_calculation_output_time_system_error(params):
    """Test errors when output time system is invalid."""
    with raises(CalculationInvalidAttr):
        Calculation(output_time_system='WRONG', **params)

    with raises(CalculationUndefinedAttr):
        # Missing 'output_sclk_id'
        Calculation(output_time_system='SPACECRAFT_CLOCK', **params)


def test_calculation_output_time_format_error(params):
    """Test errors when output time format is invalid."""
    with raises(CalculationInvalidAttr):
        Calculation(output_time_format='WRONG', **params)

    with raises(CalculationIncompatibleAttr):
        # Wrong 'output_time_system'
        Calculation(output_time_format='CALENDAR',
                    output_time_system='SPACECRAFT_CLOCK', **params)

    with raises(CalculationIncompatibleAttr):
        # Wrong 'output_time_system'
        Calculation(output_time_format='SPACECRAFT_CLOCK_STRING',
                    output_time_system='UTC', **params)


def test_calculation_output_sclk_id_error(params):
    """Test errors when output sclk id is invalid."""
    with raises(CalculationIncompatibleAttr):
        Calculation(output_sclk_id=-82, output_time_system='WRONG', **params)


def test_calculation_output_time_custom_format_error(params):
    """Test errors when output time custom is invalid."""
    with raises(CalculationIncompatibleAttr):
        Calculation(output_time_custom_format='YYYY Month DD HR:MN',
                    output_time_format='WRONG', **params)
