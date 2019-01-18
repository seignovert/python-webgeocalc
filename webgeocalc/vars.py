# -*- coding: utf-8 -*-

API_URL = 'https://wgc2.jpl.nasa.gov:8443/webgeocalc/api'

CALCULATION_TYPE = [
    'STATE_VECTOR',
    'ANGULAR_SEPARATION',
    'ANGULAR_SIZE',
    'SUB_OBSERVER_POINT',
    'SUB_SOLAR_POINT',
    'ILLUMINATION_ANGLES',
    'SURFACE_INTERCEPT_POINT',
    'OSCULATING_ELEMENTS',
    'FRAME_TRANSFORMATION',
    'GF_COORDINATE_SEARCH',
    'GF_ANGULAR_SEPARATION_SEARCH',
    'GF_DISTANCE_SEARCH',
    'GF_SUB_POINT_SEARCH',
    'GF_OCCULTATION_SEARCH',
    'GF_TARGET_IN_INSTRUMENT_FOV_SEARCH',
    'GF_SURFACE_INTERCEPT_POINT_SEARCH',
    'GF_RAY_IN_FOV_SEARCH',
    'TIME_CONVERSION',
]

TIME_SYSTEM = [
    'UTC',
    'TDB',
    'TDT',
    'SPACECRAFT_CLOCK',
]

TIME_FORMAT = [
    'CALENDAR',
    'JULIAN',
    'SECONDS_PAST_J2000',
    'SPACECRAFT_CLOCK_TICKS',
    'SPACECRAFT_CLOCK_STRING',
]

TIME_STEP_UNITS = [
    'SECONDS',
    'MINUTES',
    'HOURS',
    'DAYS',
    'EQUAL_INTERVALS',
]

INTERVALS = [
    "array([startTime, endTime])",
    "dict({'startTime': startTime, 'endTime': endTime})",
    "array([ interval1, interval2, … ])",
]

ABERRATION_CORRECTION = [
    'NONE',
    'LT',
    'LT+S',
    'CN',
    'CN+S',
    'XLT',
    'XLT+S',
    'XCN',
    'XCN+S',
]

STATE_REPRESENTATION = [
    'RECTANGULAR',
    'RA_DEC',
    'LATITUDINAL',
    'PLANETODETIC',
    'PLANETOGRAPHIC',
    'CYLINDRICAL',
    'SPHERICAL',
]
