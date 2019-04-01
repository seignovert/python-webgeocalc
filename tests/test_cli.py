# -*- coding: utf-8 -*-
'''Test WGC command line inputs.'''

from webgeocalc.cli import (_params, cli_angular_separation, cli_angular_size, cli_bodies,
                            cli_frame_transformation, cli_frames, cli_illumination_angles,
                            cli_instruments, cli_kernel_sets, cli_osculating_elements,
                            cli_state_vector, cli_subobserver_point, cli_subsolar_point,
                            cli_surface_intercept_point, cli_time_conversion)

def test_cli_kernel_sets(capsys):
    '''Test GET kernels with CLI.'''
    argv = ''.split()
    cli_kernel_sets(argv)
    captured = capsys.readouterr()
    assert 'usage:' in captured.out

    argv = '--all'.split()
    cli_kernel_sets(argv)
    captured = capsys.readouterr()
    assert ' - Solar System Kernels: (id: 1)' in captured.out
    assert ' - Cassini Huygens: (id: 5)' in captured.out

    argv = '--kernel 1 Cassini'.split()
    cli_kernel_sets(argv)
    captured = capsys.readouterr()
    assert ' - Solar System Kernels: (id: 1)' in captured.out
    assert 'Too many kernel sets contains \'Cassini\' in their names:' in captured.out

def test_cli_bodies(capsys):
    '''Test GET bodies with CLI.'''
    argv = ''.split()
    cli_bodies(argv)
    captured = capsys.readouterr()
    assert 'usage:' in captured.out

    argv = ['Cassini Huygens']
    cli_bodies(argv)
    captured = capsys.readouterr()
    assert ' - CASSINI: (id: -82)' in captured.out
    assert ' - TITAN: (id: 606)' in captured.out

    argv = '5 --name Titan'.split()
    cli_bodies(argv)
    captured = capsys.readouterr()
    assert captured.out == ' - TITAN: (id: 606)\n'

def test_cli_frames(capsys):
    '''Test GET frames with CLI.'''
    argv = ''.split()
    cli_frames(argv)
    captured = capsys.readouterr()
    assert 'usage:' in captured.out

    argv = ['Cassini Huygens']
    cli_frames(argv)
    captured = capsys.readouterr()
    assert ' - IAU_TITAN: (id: 10044)' in captured.out
    assert ' - J2000: (id: 1)' in captured.out

    argv = '5 --name Titan'.split()
    cli_frames(argv)
    captured = capsys.readouterr()
    assert ' - IAU_TITAN: (id: 10044)' in captured.out
    assert ' - J2000: (id: 1)' not in captured.out

def test_cli_instruments(capsys):
    '''Test GET instruments with CLI.'''
    argv = ''.split()
    cli_instruments(argv)
    captured = capsys.readouterr()
    assert 'usage:' in captured.out

    argv = ['Cassini Huygens']
    cli_instruments(argv)
    captured = capsys.readouterr()
    assert ' - CASSINI_ISS_WAC: (id: -82361)' in captured.out
    assert ' - CASSINI_VIMS_IR: (id: -82370)' in captured.out

    argv = '5 --name ISS'.split()
    cli_instruments(argv)
    captured = capsys.readouterr()
    assert ' - CASSINI_ISS_WAC: (id: -82361)' in captured.out
    assert ' - CASSINI_VIMS_IR: (id: -82370)' not in captured.out

def test_cli_input_parameters():
    '''Test CLI input parameters parsing.'''
    def parse(x):
        return _params(x.split())

    assert parse('--kernels 1') == {'kernels': 1}
    assert parse('--kernels=1') == {'kernels': 1}
    assert parse('--kernels= 1') == {'kernels': 1}
    assert parse('--kernels = 1') == {'kernels': 1}
    assert parse('--kernels =1') == {'kernels': 1}
    assert parse('--kernels 1 5') == {'kernels': [1, 5]}
    assert parse('--kernels=1 5') == {'kernels': [1, 5]}
    assert parse('--kernels 1,5') == {'kernels': [1, 5]}
    assert parse('--kernels=1,5') == {'kernels': [1, 5]}
    assert parse('--kernels 1, 5') == {'kernels': [1, 5]}
    assert parse('--kernels=1, 5') == {'kernels': [1, 5]}
    assert parse('--kernels [1,5]') == {'kernels': [1, 5]}
    assert parse('--kernels=[1,5]') == {'kernels': [1, 5]}
    assert parse('--kernels [1, 5]') == {'kernels': [1, 5]}
    assert parse('--kernels=[1, 5]') == {'kernels': [1, 5]}
    assert parse('--kernels [ 1,5]') == {'kernels': [1, 5]}
    assert parse('--kernels=[ 1,5]') == {'kernels': [1, 5]}
    assert parse('--kernels [ 1, 5]') == {'kernels': [1, 5]}
    assert parse('--kernels [ 1, 5 ]') == {'kernels': [1, 5]}
    assert parse('--kernels [1, 5 ]') == {'kernels': [1, 5]}
    assert parse('--kernels [1,5 ]') == {'kernels': [1, 5]}
    assert parse('--kernels=[1,5 ]') == {'kernels': [1, 5]}
    assert parse('--kernels [1 ,5]') == {'kernels': [1, 5]}
    assert parse('--kernels [1 , 5]') == {'kernels': [1, 5]}
    assert parse('--kernels [1, 3, 5]') == {'kernels': [1, 3, 5]}
    assert parse('--kernels 1, 3, 5') == {'kernels': [1, 3, 5]}
    assert parse('--kernels 1 --kernels 5') == {'kernels': [1, 5]}
    assert parse('--kernels=1 --kernels 5') == {'kernels': [1, 5]}
    assert parse('--kernels=1 --kernels=5') == {'kernels': [1, 5]}
    assert parse('null --kernels=1') == {'kernels': 1}

    assert parse('--kernels Cassini') == {'kernels': 'Cassini'}
    assert parse("--kernels 'Cassini'") == {'kernels': 'Cassini'}
    assert parse('--kernels "Cassini"') == {'kernels': 'Cassini'}
    assert parse('--kernels "Cassini" "Solar"') == {'kernels': ['Cassini', 'Solar']}

    assert parse("--times '2012-10-19T08:24:00'") == {'times': '2012-10-19T08:24:00'}

def test_cli_state_vector_empty(capsys):
    '''Test empty state vector calculation parameter with the CLI.'''
    argv = ''.split()
    cli_state_vector(argv)
    captured = capsys.readouterr()
    assert 'usage:' in captured.out

def test_cli_angular_separation_wrong_attr(capsys):
    '''Test attribute in angular separation calculation parameter with the CLI.'''
    argv = '--wrong 123'.split()
    cli_angular_separation(argv)
    captured = capsys.readouterr()
    assert captured.out == 'Attribute \'target_1\' required.\n'

def test_cli_angular_size_run(capsys):
    '''Test run angular size calculation parameter with the CLI.'''
    argv = ('--payload '
            '--kernels 5 '
            '--times 2012-10-19T08:24:00 '
            '--target ENCELADUS '
            '--observer CASSINI '
            '--aberration_correction CN+S').split()

    cli_angular_size(argv)
    captured = capsys.readouterr()
    assert 'Payload:' in captured.out
    assert "kernels: [{'type': 'KERNEL_SET', 'id': 5}]," in captured.out
    assert "times: ['2012-10-19T08:24:00']," in captured.out
    assert "calculationType: ANGULAR_SIZE," in captured.out
    assert "timeSystem: UTC," in captured.out
    assert 'API status:\n[Calculation submit] Phase:' in captured.out
    assert 'Results:\nDATE:\n> 2012-10-19 08:24:00.000000 UTC' in captured.out
    assert 'ANGULAR_SIZE:\n> 0.03037939' in captured.out

def test_cli_frame_transformation_dry_run(capsys):
    '''Test dry-run frame transform calculation parameter with the CLI.'''
    argv = ('--dry-run '
            '--kernels 5 '
            '--times 2012-10-19T08:24:00.000 '
            '--frame_1 IAU_SATURN '
            '--frame_2 IAU_ENCELADUS '
            '--aberration_correction NONE').split()

    cli_frame_transformation(argv)
    captured = capsys.readouterr()
    assert 'Payload:' in captured.out
    assert "calculationType: FRAME_TRANSFORMATION," in captured.out
    assert 'API status:\n[Calculation submit] Status:' not in captured.out
    assert 'Results:' not in captured.out

def test_cli_illumination_angles_dry_run(capsys):
    '''Test dry-run illumination angles calculation parameter with the CLI.'''
    argv = ('--dry-run '
            '--kernels 5 '
            '--times 2012-10-19T08:24:00.000 '
            '--target ENCELADUS '
            '--target_frame IAU_ENCELADUS '
            '--observer CASSINI '
            '--aberration_correction CN+S '
            '--latitude 0.0 '
            '--longitude 0.0').split()

    cli_illumination_angles(argv)
    captured = capsys.readouterr()
    assert 'Payload:' in captured.out
    assert "calculationType: ILLUMINATION_ANGLES," in captured.out

def test_cli_subsolar_point_dry_run(capsys):
    '''Test dry-run sub-solar point calculation parameter with the CLI.'''
    argv = ('--dry-run '
            '--kernels 5 '
            '--times 2012-10-19T08:24:00.000 '
            '--target ENCELADUS '
            '--target_frame IAU_ENCELADUS '
            '--observer CASSINI '
            '--aberration_correction CN+S').split()

    cli_subsolar_point(argv)
    captured = capsys.readouterr()
    assert 'Payload:' in captured.out
    assert "calculationType: SUB_SOLAR_POINT," in captured.out

def test_cli_subobserver_point_dry_run(capsys):
    '''Test dry-run sub-observer point calculation parameter with the CLI.'''
    argv = ('--dry-run '
            '--kernels 5 '
            '--times 2012-10-19T08:24:00.000 '
            '--target ENCELADUS '
            '--target_frame IAU_ENCELADUS '
            '--observer CASSINI '
            '--aberration_correction CN+S').split()

    cli_subobserver_point(argv)
    captured = capsys.readouterr()
    assert 'Payload:' in captured.out
    assert "calculationType: SUB_OBSERVER_POINT," in captured.out

def test_cli_surface_intercept_point_dry_run(capsys):
    '''Test dry-run surface intercept point calculation parameter with the CLI.'''
    argv = ('--dry-run '
            '--kernels 5 '
            '--times 2012-10-19T08:24:00.000 '
            '--target SATURN '
            '--target_frame IAU_SATURN '
            '--observer CASSINI '
            '--direction_vector_type INSTRUMENT_BORESIGHT '
            '--direction_instrument CASSINI_ISS_NAC '
            '--aberration_correction NONE '
            '--state_representation LATITUDINAL').split()

    cli_surface_intercept_point(argv)
    captured = capsys.readouterr()
    assert 'Payload:' in captured.out
    assert "calculationType: SURFACE_INTERCEPT_POINT," in captured.out

def test_cli_osculating_elements_dry_run(capsys):
    '''Test dry-run osculating elements calculation parameter with the CLI.'''
    argv = ('--dry-run '
            '--kernels 1 5 '
            '--times 2012-10-19T08:24:00.000 '
            '--orbiting_body CASSINI '
            '--center_body SATURN').split()

    cli_osculating_elements(argv)
    captured = capsys.readouterr()
    assert 'Payload:' in captured.out
    assert "calculationType: OSCULATING_ELEMENTS," in captured.out

def test_cli_time_conversion_dry_run(capsys):
    '''Test dry-run time conversion calculation parameter with the CLI.'''
    argv = ('--dry-run '
            '--kernels 5 '
            '--times 1/1729329441.04 '
            '--time_system SPACECRAFT_CLOCK '
            '--time_format SPACECRAFT_CLOCK_STRING '
            '--sclk_id -82 '
            ).split()

    cli_time_conversion(argv)
    captured = capsys.readouterr()
    assert 'Payload:' in captured.out
    assert "calculationType: TIME_CONVERSION," in captured.out
