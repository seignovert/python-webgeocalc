"""Test WGC command line inputs."""

from webgeocalc.cli import (_params, cli_angular_separation, cli_angular_size,
                            cli_bodies, cli_frame_transformation, cli_frames,
                            cli_gf_coordinate_search, cli_illumination_angles,
                            cli_instruments, cli_kernel_sets,
                            cli_osculating_elements, cli_phase_angle, cli_state_vector,
                            cli_subobserver_point, cli_subsolar_point,
                            cli_surface_intercept_point, cli_time_conversion)


def test_cli_kernel_sets(capsys):
    """Test GET kernels with CLI."""
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

    argv = '--api esa --kernel 13'.split()
    cli_kernel_sets(argv)
    captured = capsys.readouterr()
    assert ' - OPS  --     Rosetta               -- Operational: (id: 13)' in captured.out
    assert '' in captured.out


def test_cli_bodies(capsys):
    """Test GET bodies with CLI."""
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

    argv = '--api esa 13 --name 67P'.split()
    cli_bodies(argv)
    captured = capsys.readouterr()
    assert captured.out == ' - 67P/CHURYUMOV-GERASIMENKO (1969 R1): (id: 1000012)\n'


def test_cli_frames(capsys):
    """Test GET frames with CLI."""
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

    argv = '--api esa 13 --name 67P'.split()
    cli_frames(argv)
    captured = capsys.readouterr()
    assert '- 67P/C-G_CK: (id: -1000012000)' in captured.out
    assert ' - J2000: (id: 1)' not in captured.out


def test_cli_instruments(capsys):
    """Test GET instruments with CLI."""
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

    argv = '--api esa 13 --name NAVCAM'.split()
    cli_instruments(argv)
    captured = capsys.readouterr()
    assert ' - ROS_NAVCAM-A: (id: -226170)' in captured.out
    assert ' - ROS_NAVCAM-B: (id: -226180)' in captured.out
    assert ' - ROS_CONSERT: (id: -226160)' not in captured.out


def test_cli_input_parameters():
    """Test CLI input parameters parsing."""
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
    assert parse("--times 2000-01-01 --times 2000-01-02'") == {
        'times': ['2000-01-01', '2000-01-02']
    }


def test_cli_input_parameters_nested():
    """Test CLI nested input parameters parsing."""
    # Double quotes
    assert _params([
        '--double-quotes',
        '"direction_type=POSITION target=SUN shape=POINT observer=\'CASSINI\'"',
    ]) == {
        'double_quotes': {
            'direction_type': 'POSITION',
            'target': 'SUN',
            'shape': 'POINT',
            'observer': 'CASSINI',
        }
    }

    # Single quote
    assert _params([
        '--single-quote',
        "'direction_type=VECTOR direction_vector_type=REFERENCE_FRAME_AXIS"
        " direction_frame=\"CASSINI_RPWS_EDIPOLE\" direction_frame_axis=Z'",
    ]) == {
        'single_quote': {
            'direction_type': 'VECTOR',
            'direction_vector_type': 'REFERENCE_FRAME_AXIS',
            'direction_frame': 'CASSINI_RPWS_EDIPOLE',
            'direction_frame_axis': 'Z',
        }
    }


def test_cli_state_vector_empty(capsys):
    """Test empty state vector calculation parameter with the CLI."""
    argv = ''.split()
    cli_state_vector(argv)
    captured = capsys.readouterr()
    assert 'usage:' in captured.out


def test_cli_state_vector_esa(capsys):
    """Test dry-run state vector calculation on ESA API with the CLI."""
    argv = [
        '--dry-run',
        '--api', 'ESA',
        '--kernels', '"OPS  --     Rosetta"',
        '--times', '2014-01-01T01:23:45.000',
        '--calculation_type', 'STATE_VECTOR',
        '--target', '"67P/CHURYUMOV-GERASIMENKO (1969 R1)"',
        '--observer', '"ROSETTA ORBITER"',
        '--reference_frame', '"67P/C-G_CK"',
        '--aberration_correction', 'NONE',
        '--state_representation', 'LATITUDINAL',
    ]

    cli_state_vector(argv)
    captured = capsys.readouterr()
    assert 'API: http://spice.esac.esa.int/webgeocalc/api' in captured.out
    assert 'Payload:' in captured.out
    assert "kernels: [{'type': 'KERNEL_SET', 'id': 13}]" in captured.out
    assert "times: ['2014-01-01T01:23:45.000']" in captured.out
    assert 'target: 67P/CHURYUMOV-GERASIMENKO (1969 R1)' in captured.out
    assert 'observer: ROSETTA ORBITER' in captured.out
    assert 'referenceFrame: 67P/C-G_CK' in captured.out
    assert 'calculationType: STATE_VECTOR' in captured.out
    assert 'aberrationCorrection: NONE' in captured.out
    assert 'stateRepresentation: LATITUDINAL' in captured.out
    assert 'timeSystem: UTC' in captured.out
    assert 'timeFormat: CALENDAR' in captured.out


def test_cli_angular_separation_two_targets_dry_run(capsys):
    """Test dry-run angular separation calculation for 2 targets with the CLI."""
    argv = ('--dry-run '
            '--kernels 5 '
            '--times 2012-10-19T08:24:00 '
            '--target_1 VENUS '
            '--target_2 MERCURY '
            '--observer SUN').split()

    cli_angular_separation(argv)
    captured = capsys.readouterr()
    assert 'Payload:' in captured.out
    assert "kernels: [{'type': 'KERNEL_SET', 'id': 5}]" in captured.out
    assert "times: ['2012-10-19T08:24:00']" in captured.out
    assert 'target1: VENUS' in captured.out
    assert 'shape1: POINT' in captured.out
    assert 'target2: MERCURY' in captured.out
    assert 'shape2: POINT' in captured.out
    assert 'observer: SUN' in captured.out
    assert 'timeSystem: UTC' in captured.out
    assert 'aberrationCorrection: CN' in captured.out
    assert 'timeFormat: CALENDAR' in captured.out


def test_cli_angular_separation_two_directions_dry_run(capsys):
    """Test dry-run angular separation calculation for 2 direction with the CLI."""
    argv = [
        '--dry-run',
        '--kernels', '5',
        '--times', '2012-10-19T08:24:00',
        '--spec_type', 'TWO_DIRECTIONS',
        # double quotes
        '--direction_1', '"direction_type=POSITION '
        'target=SUN '
        'shape=POINT '
        'observer=\'CASSINI\'"',
        # single quote
        '--direction_2', "'direction_type=VECTOR "
        "direction_vector_type=REFERENCE_FRAME_AXIS "
        "direction_frame=\"CASSINI_RPWS_EDIPOLE\" "
        "direction_frame_axis=Z'",
    ]

    cli_angular_separation(argv)
    captured = capsys.readouterr()
    assert 'Payload:' in captured.out
    assert "calculationType: ANGULAR_SEPARATION" in captured.out
    assert "kernels: [{'type': 'KERNEL_SET', 'id': 5}]" in captured.out
    assert "times: ['2012-10-19T08:24:00']" in captured.out
    assert "specType: TWO_DIRECTIONS" in captured.out
    assert (
        "direction1: {"
        "'directionType': 'POSITION', "
        "'target': 'SUN', "
        "'shape': 'POINT', "
        "'observer': 'CASSINI', "
        "'aberrationCorrection': 'NONE', "
        "'antiVectorFlag': False"
        "}"
    ) in captured.out
    assert (
        "direction2: {"
        "'directionType': 'VECTOR', "
        "'directionVectorType': 'REFERENCE_FRAME_AXIS', "
        "'directionFrame': 'CASSINI_RPWS_EDIPOLE', "
        "'directionFrameAxis': 'Z', "
        "'aberrationCorrection': 'NONE', "
        "'antiVectorFlag': False"
        "}"
    ) in captured.out
    assert 'timeSystem: UTC' in captured.out
    assert 'timeFormat: CALENDAR' in captured.out


def test_cli_angular_separation_wrong_attr(capsys):
    """Test attribute in angular separation calculation parameter with the CLI."""
    argv = '--kernels 1 --times 2012-10-19T08:24:00 --wrong 123'.split()
    cli_angular_separation(argv)
    captured = capsys.readouterr()
    assert captured.out == 'Attribute \'target_1\' required.\n'


def test_cli_angular_size_run(capsys):
    """Test run angular size calculation parameter with the CLI."""
    argv = ('--payload '
            '--kernels 5 '
            '--times 2012-10-19T08:24:00 '
            '--target ENCELADUS '
            '--observer CASSINI '
            '--aberration_correction CN+S').split()

    cli_angular_size(argv)
    captured = capsys.readouterr()
    assert 'API: https://wgc2.jpl.nasa.gov:8443/webgeocalc/api' in captured.out
    assert 'Payload:' in captured.out
    assert "kernels: [{'type': 'KERNEL_SET', 'id': 5}]," in captured.out
    assert "times: ['2012-10-19T08:24:00']," in captured.out
    assert "calculationType: ANGULAR_SIZE," in captured.out
    assert "timeSystem: UTC," in captured.out
    assert 'API status:\n[Calculation submit] Phase:' in captured.out
    assert 'Results:\nDATE:\n> 2012-10-19 08:24:00.000000 UTC' in captured.out
    assert 'ANGULAR_SIZE:\n> 0.03032491' in captured.out


def test_cli_frame_transformation_dry_run(capsys):
    """Test dry-run frame transform calculation parameter with the CLI."""
    argv = ('--dry-run '
            '--kernels 5 '
            '--times 2012-10-19T08:24:00.000 '
            '--frame_1 IAU_SATURN '
            '--frame_2 IAU_ENCELADUS '
            '--aberration_correction NONE').split()

    cli_frame_transformation(argv)
    captured = capsys.readouterr()
    assert 'API: https://wgc2.jpl.nasa.gov:8443/webgeocalc/api' in captured.out
    assert 'Payload:' in captured.out
    assert "calculationType: FRAME_TRANSFORMATION," in captured.out
    assert 'API status:\n[Calculation submit] Status:' not in captured.out
    assert 'Results:' not in captured.out


def test_cli_illumination_angles_dry_run(capsys):
    """Test dry-run illumination angles calculation parameter with the CLI."""
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


def test_cli_phase_angle_dry_run(capsys):
    """Test dry-run phase angle calculation parameter with the CLI."""
    argv = ('--dry-run '
            '--kernels 5 '
            '--times 2012-10-19T08:24:00.000 '
            '--target ENCELADUS '
            '--observer CASSINI '
            '--aberration_correction CN+S ').split()

    cli_phase_angle(argv)
    captured = capsys.readouterr()
    assert 'Payload:' in captured.out
    assert "calculationType: PHASE_ANGLE," in captured.out
    assert "target: ENCELADUS" in captured.out
    assert "observer: CASSINI" in captured.out
    assert "illuminator: SUN" in captured.out
    assert "aberrationCorrection: CN+S" in captured.out


def test_cli_subsolar_point_dry_run(capsys):
    """Test dry-run sub-solar point calculation parameter with the CLI."""
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
    """Test dry-run sub-observer point calculation parameter with the CLI."""
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
    """Test dry-run surface intercept point calculation parameter with the CLI."""
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
    """Test dry-run osculating elements calculation parameter with the CLI."""
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
    """Test dry-run time conversion calculation parameter with the CLI."""
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


def test_cli_gf_coordinate_search_dry_run(capsys):
    """Test dry-run geometry finder coordinate search parameter with the CLI."""
    argv = ('--dry-run '
            '--kernels 5 '
            '--intervals 2012-10-19T07:00:00 2012-10-19T09:00:00 '
            '--observer CASSINI '
            '--target ENCELADUS '
            '--reference_frame CASSINI_ISS_NAC '
            '--time_step 1 '
            '--time_step_units MINUTES '
            '--aberration_correction NONE '
            '--interval_adjustment EXPAND_INTERVALS '
            '--interval_adjustment_amount 1.0 '
            '--interval_adjustment_units SECONDS '
            '--interval_filtering FILTER_INTERVALS '
            '--interval_filtering_threshold 1.0 '
            '--interval_filtering_threshold_units MINUTES '
            '--coordinate_system SPHERICAL '
            '--coordinate COLATITUDE '
            '--relational_condition "<" '
            '--reference_value 0.25 '
            ).split()

    cli_gf_coordinate_search(argv)
    captured = capsys.readouterr()
    assert 'Payload:' in captured.out
    assert "calculationType: GF_COORDINATE_SEARCH," in captured.out
    assert "kernels: [{'type': 'KERNEL_SET', 'id': 5}]" in captured.out
    assert 'timeSystem: UTC' in captured.out
    assert 'timeFormat: CALENDAR' in captured.out
    assert ("intervals: [{"
            "'startTime': '2012-10-19T07:00:00', "
            "'endTime': '2012-10-19T09:00:00'"
            "}]") in captured.out
    assert 'target: ENCELADUS,' in captured.out
    assert 'observer: CASSINI,' in captured.out
    assert 'referenceFrame: CASSINI_ISS_NAC,' in captured.out
    assert 'timeStep: 1,' in captured.out
    assert 'timeStepUnits: MINUTES,' in captured.out
    assert 'aberrationCorrection: NONE' in captured.out
    assert 'outputDurationUnits: SECONDS' in captured.out
    assert 'shouldComplementWindow: False' in captured.out
    assert 'intervalAdjustment: EXPAND_INTERVALS' in captured.out
    assert 'intervalAdjustmentAmount: 1.0' in captured.out
    assert 'intervalAdjustmentUnits: SECONDS' in captured.out
    assert 'intervalFiltering: FILTER_INTERVALS' in captured.out
    assert 'intervalFilteringThreshold: 1.0' in captured.out
    assert 'intervalFilteringThresholdUnits: MINUTES' in captured.out
    assert ("condition: {"
            "'coordinateSystem': 'SPHERICAL', "
            "'coordinate': 'COLATITUDE', "
            "'relationalCondition': '<', "
            "'referenceValue': 0.25"
            "}") in captured.out
