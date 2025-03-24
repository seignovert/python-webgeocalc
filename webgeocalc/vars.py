"""WebGeoCalc variables."""

JPL_URL = 'https://wgc2.jpl.nasa.gov:8443/webgeocalc/api'
ESA_URL = 'http://spice.esac.esa.int/webgeocalc/api'

CALCULATION_FAILED_PHASES = [
    'FAILED',
    'CANCELLED',
    'DISPATCHED',
    'EXPIRED',
]

VALID_PARAMETERS = {
    'CALCULATION_TYPE': [
        'STATE_VECTOR',
        'ANGULAR_SEPARATION',
        'ANGULAR_SIZE',
        'FRAME_TRANSFORMATION',
        'ILLUMINATION_ANGLES',
        'PHASE_ANGLE',
        'POINTING_DIRECTION',
        'SUB_SOLAR_POINT',
        'SUB_OBSERVER_POINT',
        'SURFACE_INTERCEPT_POINT',
        # 'TANGENT_POINT',
        'OSCULATING_ELEMENTS',
        'GF_COORDINATE_SEARCH',
        # 'GF_ANGULAR_SEPARATION_SEARCH',
        # 'GF_DISTANCE_SEARCH',
        # 'GF_SUB_POINT_SEARCH',
        # 'GF_OCCULTATION_SEARCH',
        # 'GF_SURFACE_INTERCEPT_POINT_SEARCH',
        # 'GF_TARGET_IN_INSTRUMENT_FOV_SEARCH',
        # 'GF_RAY_IN_FOV_SEARCH',
        # 'GF_RANGE_RATE_SEARCH',
        # 'GF_PHASE_ANGLE_SEARCH',
        # 'GF_ILLUMINATION_ANGLES_SEARCH',
        'TIME_CONVERSION',
    ],
    'TIME_SYSTEM': [
        'UTC',
        'TDB',
        'TDT',
        'SPACECRAFT_CLOCK',
    ],
    'TIME_FORMAT': [
        'CALENDAR',
        'JULIAN',
        'SECONDS_PAST_J2000',
        'SPACECRAFT_CLOCK_TICKS',
        'SPACECRAFT_CLOCK_STRING',
    ],
    'OUTPUT_TIME_FORMAT': [
        'CALENDAR',
        'CALENDAR_YMD',
        'CALENDAR_DOY',
        'JULIAN',
        'SECONDS_PAST_J2000',
        'SPACECRAFT_CLOCK_STRING',
        'SPACECRAFT_CLOCK_TICKS',
        'CUSTOM',
    ],
    'TIME_UNITS': [
        'SECONDS',
        'MINUTES',
        'HOURS',
        'DAYS',
    ],
    'TIME_STEP_UNITS': [
        'SECONDS',
        'MINUTES',
        'HOURS',
        'DAYS',
        'EQUAL_INTERVALS'
    ],
    'INTERVALS': [
        "array([startTime, endTime])",
        "dict({'startTime': startTime, 'endTime': endTime})",
        "array([ interval1, interval2, … ])",
    ],
    'ABERRATION_CORRECTION': [
        'NONE',
        'LT',
        'LT+S',
        'CN',
        'CN+S',
        'XLT',
        'XLT+S',
        'XCN',
        'XCN+S',
    ],
    'ABERRATION_CORRECTION_NO_S': [
        'NONE',
        'LT',
        'CN',
        'XLT',
        'XCN',
    ],
    'ABERRATION_CORRECTION_NO_X': [
        'NONE',
        'LT',
        'LT+S',
        'CN',
        'CN+S',
    ],
    'ABERRATION_CORRECTION_VECTOR': [
        'NONE',
        'LT',
        'CN',
        'XLT',
        'XCN',
        'S',
        'XS',
    ],
    'SPEC_TYPE': [
        'TWO_TARGETS',
        'TWO_DIRECTIONS',
    ],
    'STATE_REPRESENTATION': [
        'RECTANGULAR',
        'RA_DEC',
        'LATITUDINAL',
        'PLANETODETIC',
        'PLANETOGRAPHIC',
        'CYLINDRICAL',
        'SPHERICAL',
    ],
    'SHAPE': [
        'POINT',
        'SPHERE',
        'ELLIPSOID',
        'DSK ',
    ],
    'TARGET_SHAPE': [
        'POINT',
        'SPHERE',
    ],
    'TIME_LOCATION': [
        'FRAME1',
        'FRAME2',
    ],
    'ORIENTATION_REPRESENTATION': [
        'EULER_ANGLES',
        'ANGLE_AND_AXIS',
        'SPICE_QUATERNION',
        'OTHER_QUATERNION',
        'MATRIX_ROW_BY_ROW',
        'MATRIX_FLAGGED',
        'MATRIX_ALL_ONE_ROW',
    ],
    'ANGULAR_VELOCITY_REPRESENTATION': [
        'NOT_INCLUDED',
        'VECTOR_IN_FRAME1',
        'VECTOR_IN_FRAME2',
        'EULER_ANGLE_DERIVATIVES',
        'MATRIX',
    ],
    'AXIS': [
        'X',
        'Y',
        'Z',
    ],
    'ANGULAR_UNITS': [
        'deg',
        'rad',
    ],
    'ANGULAR_VELOCITY_UNITS': [
        'deg/s',
        'rad/s',
        'RPM',
        'Unitary',
    ],
    'COORDINATE_REPRESENTATION': [
        'RECTANGULAR',
        'RA_DEC',
        'LATITUDINAL',  # (planetocentric)
        'PLANETODETIC',
        'PLANETOGRAPHIC',
        'CYLINDRICAL',
        'SPHERICAL',
        'AZ_EL',
    ],
    'COORDINATE_REPRESENTATION_POINTING_DIRECTION': [
        'RECTANGULAR',
        'RA_DEC',
        'LATITUDINAL',  # (planetocentric)
        'CYLINDRICAL',
        'SPHERICAL',
        'AZ_EL',
    ],
    'SUB_POINT_TYPE': [
        'Near point: ellipsoid',
        'Intercept: ellipsoid',
        'NADIR/DSK/UNPRIORITIZED',
        'INTERCEPT/DSK/UNPRIORITIZED',
    ],
    'INTERVAL_ADJUSTMENT': [
        'NO_ADJUSTMENT',
        'EXPAND_INTERVALS',
        'CONTRACT_INTERVALS',
    ],
    'INTERVAL_FILTERING': [
        'NO_FILTERING',
        'FILTER_INTERVALS',
        'OMIT_INTERVALS_SMALLER_THAN_A_THRESHOLD',
    ],
    'COORDINATE_SYSTEM': [
        'RECTANGULAR',
        'RA/DEC',
        'LATITUDINAL',
        'CYLINDRICAL',
        'SPHERICAL',
        'GEODETIC',
        'PLANETOGRAPHIC',
    ],
    'COORDINATE': [
        'X',
        'Y',
        'Z',
        'LONGITUDE',
        'LATITUDE',
        'COLATITUDE',
        'RIGHT ASCENSION',
        'DECLINATION',
        'RANGE',
        'RADIUS',
        'ALTITUDE',
    ],
    'RELATIONAL_CONDITION': [
        '=',
        '<',
        '>',
        'RANGE',
        'ABSMAX',
        'ABSMIN',
        'LOCMAX',
        'LOCMIN',
    ],
    'DIRECTION_TYPE': [
        'POSITION',
        'VELOCITY',
        'VECTOR',
    ],
    'BOOLEAN': [
        True,
        False,
        'true',
        'false',
        'True',
        'False',
        'TRUE',
        'FALSE',
    ],
    'DIRECTION_VECTOR_TYPE': [
        'INSTRUMENT_BORESIGHT',
        'REFERENCE_FRAME_AXIS',
        'VECTOR_IN_INSTRUMENT_FOV',
        'VECTOR_IN_REFERENCE_FRAME',
        'INSTRUMENT_FOV_BOUNDARY_VECTORS',
    ],
    'VECTOR_MAGNITUDE': [
        'UNIT',
        'PRESERVE_ORIGINAL',
    ]
}
