"""Test WGC geometry finder errors."""

from pytest import raises

from webgeocalc import GFAngularSeparationSearch
from webgeocalc.cli import (
    cli_gf_angular_separation_search,
    cli_gf_distance_search,
    cli_gf_illumination_angles_search,
    cli_gf_occultation_search,
    cli_gf_phase_angle_search,
    cli_gf_range_rate_search,
    cli_gf_ray_in_fov_search,
    cli_gf_sub_point_search,
    cli_gf_surface_intercept_point_search,
    cli_gf_target_in_instrument_fov_search,
)


def test_gf_not_implemented_errors():
    """Test geometry finder not implemented errors."""
    with raises(NotImplementedError):
        GFAngularSeparationSearch()


def test_gf_cli_errors():
    """Test geometry finder searches errors in CLI."""
    with raises(NotImplementedError):
        cli_gf_angular_separation_search(['--kernels', '5'])

    with raises(NotImplementedError):
        cli_gf_distance_search(['--kernels', '5'])

    with raises(NotImplementedError):
        cli_gf_sub_point_search(['--kernels', '5'])

    with raises(NotImplementedError):
        cli_gf_occultation_search(['--kernels', '5'])

    with raises(NotImplementedError):
        cli_gf_surface_intercept_point_search(['--kernels', '5'])

    with raises(NotImplementedError):
        cli_gf_target_in_instrument_fov_search(['--kernels', '5'])

    with raises(NotImplementedError):
        cli_gf_ray_in_fov_search(['--kernels', '5'])

    with raises(NotImplementedError):
        cli_gf_range_rate_search(['--kernels', '5'])

    with raises(NotImplementedError):
        cli_gf_phase_angle_search(['--kernels', '5'])

    with raises(NotImplementedError):
        cli_gf_illumination_angles_search(['--kernels', '5'])
