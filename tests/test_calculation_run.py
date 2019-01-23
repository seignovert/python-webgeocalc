# -*- coding: utf-8 -*-
import pytest
import requests_mock

from webgeocalc import Calculation, StateVector
from webgeocalc.vars import API_URL
from webgeocalc.errors import CalculationNotCompleted, CalculationAlreadySubmitted, ResultAttributeError

@pytest.fixture
def params():
    return {
        "calculation_type": "STATE_VECTOR",
        "kernels": 1,
        "time_system": "UTC",
        "time_format": "CALENDAR",
        "intervals": ["2000-01-01", "2000-01-02"],
        "time_step": 30,
        "time_step_units": "MINUTES",
        "target": "SUN",
        "observer": "EARTH",
        "reference_frame": "J2000",
        "aberration_correction": "NONE",
        "state_representation": "RA_DEC"
    }

@pytest.fixture
def response():
    return {
        "status": "OK",
        "message": "The operation was successful.",
        "calculationId": "0788aba2-d4e5-4028-9ef1-4867ad5385e0",
        "result": {
            "phase": "COMPLETE",
            "progress": 0
        }
    }


@pytest.fixture
def results():
    return {
        "status": "OK",
        "message": "The operation was successful.",
        "calculationId": "0788aba2-d4e5-4028-9ef1-4867ad5385e0",
        "columns": [
            {
                "name": "UTC calendar date",
                "type": "DATE",
                "outputID": "DATE",
                "units": ""
            },
            {
                "name": "Right Ascension (deg)",
                "type": "NUMBER",
                "outputID": "RIGHT_ASCENSION",
                "units": "deg"
            },
            {
                "name": "Declination (deg)",
                "type": "NUMBER",
                "outputID": "DECLINATION",
                "units": "deg"
            },
            {
                "name": "Range (km)",
                "type": "NUMBER",
                "outputID": "RANGE",
                "units": "km"
            },
            {
                "name": "d Right Ascension/dt (deg/s)",
                "type": "NUMBER",
                "outputID": "D_RIGHT_ASCENSION_DT",
                "units": "deg/s"
            },
            {
                "name": "d Declination/dt (deg/s)",
                "type": "NUMBER",
                "outputID": "D_DECLINATION_DT",
                "units": "deg/s"
            },
            {
                "name": "d Range/dt (km/s)",
                "type": "NUMBER",
                "outputID": "D_RANGE_DT",
                "units": "km/s"
            },
            {
                "name": "Speed (km/s)",
                "type": "NUMBER",
                "outputID": "SPEED",
                "units": "km/s"
            },
            {
                "name": "Time at Target",
                "type": "DATE",
                "outputID": "TIME_AT_TARGET",
                "units": ""
            },
            {
                "name": "Light Time (s)",
                "type": "NUMBER",
                "outputID": "LIGHT_TIME",
                "units": "s"
            }
        ],
        "rows": [
            [
                "2000-01-01 00:00:00.000000 UTC",
                280.73666816,
                -23.07197828,
                147104359.15044397,
                0.0000127884715,
                8.74255781e-7,
                -0.01659221,
                30.29084386,
                "2000-01-01 00:00:00.000000 UTC",
                490.6873246
            ],
            [
                "2000-01-02 00:00:00.000000 UTC",
                281.84100169,
                -22.99260787,
                147103258.34983575,
                0.0000127745341,
                9.62949471e-7,
                -0.00894244,
                30.29324424,
                "2000-01-02 00:00:00.000000 UTC",
                490.68365272
            ]
        ]
    }


@pytest.fixture
def params_sv():
    return {
        "kernels": 5,
        "times": "2012-10-19T08:24:00.000",
        "target": "ENCELADUS",
        "observer": "CASSINI",
        "reference_frame": "CASSINI_ISS_NAC",
    }

@pytest.fixture
def response_sv():
    return {
        "status": "OK",
        "message": "The operation was successful.",
        "calculationId": "5d009079-aa9e-4fbd-93c3-58b5a4990a68",
        "result": {
            "phase": "COMPLETE",
            "progress": 0
        }
    }

@pytest.fixture
def results_sv():
    return {
        "status": "OK",
        "message": "The operation was successful.",
        "calculationId": "5d009079-aa9e-4fbd-93c3-58b5a4990a68",
        "columns": [
            {
                "name": "UTC calendar date",
                "type": "DATE",
                "outputID": "DATE",
                "units": ""
            },
            {
                "name": "Distance (km)",
                "type": "NUMBER",
                "outputID": "DISTANCE",
                "units": "km"
            },
            {
                "name": "Speed (km/s)",
                "type": "NUMBER",
                "outputID": "SPEED",
                "units": "km/s"
            },
            {
                "name": "X (km)",
                "type": "NUMBER",
                "outputID": "X",
                "units": "km"
            },
            {
                "name": "Y (km)",
                "type": "NUMBER",
                "outputID": "Y",
                "units": "km"
            },
            {
                "name": "Z (km)",
                "type": "NUMBER",
                "outputID": "Z",
                "units": "km"
            },
            {
                "name": "dX/dt (km/s)",
                "type": "NUMBER",
                "outputID": "D_X_DT",
                "units": "km/s"
            },
            {
                "name": "dY/dt (km/s)",
                "type": "NUMBER",
                "outputID": "D_Y_DT",
                "units": "km/s"
            },
            {
                "name": "dZ/dt (km/s)",
                "type": "NUMBER",
                "outputID": "D_Z_DT",
                "units": "km/s"
            },
            {
                "name": "Time at Target",
                "type": "DATE",
                "outputID": "TIME_AT_TARGET",
                "units": ""
            },
            {
                "name": "Light Time (s)",
                "type": "NUMBER",
                "outputID": "LIGHT_TIME",
                "units": "s"
            }
        ],
        "rows": [
            [
                "2012-10-19 08:24:00.000000 UTC",
                967899.52452788,
                12.31257026,
                -112.54927003,
                -316.50526854,
                967899.4662352,
                9.20424051,
                7.86483252,
                2.24181902,
                "2012-10-19 08:23:56.771435 UTC",
                3.22856529
            ]
        ]
    }


def test_calculation_run(requests_mock, params, response, results):
    calc = Calculation(**params)

    requests_mock.post(API_URL + '/calculation/new', json=response)
    requests_mock.get(API_URL + '/calculation/' + response['calculationId'], json=response)
    requests_mock.get(API_URL + '/calculation/' + response['calculationId'] + '/results', json=results)

    with pytest.raises(CalculationNotCompleted):
        calc.results

    calc.run()
    assert calc.id == response['calculationId']


    calc.update()
    assert calc.status == response['result']['phase']

    with pytest.raises(CalculationAlreadySubmitted):
        calc.submit()
    
    calc.resubmit()
    assert calc.id == response['calculationId']

    out = calc.run() # Re-run results without API request
    assert len(out['DATE']) == len(results['rows'])

def test_state_vector_single_time(requests_mock, params_sv, response_sv, results_sv):
    sv = StateVector(**params_sv)

    requests_mock.post(API_URL + '/calculation/new', json=response_sv)
    requests_mock.get(API_URL + '/calculation/' + response_sv['calculationId'], json=response_sv)
    requests_mock.get(API_URL + '/calculation/' + response_sv['calculationId'] + '/results', json=results_sv)

    out = sv.run()
    assert out['DATE'] == results_sv['rows'][0][0]
    
    column = sv.columns[0]
    column_sv = results_sv['columns'][0]

    assert str(column) == column_sv['name']

    for key in column.keys():
        assert key in column_sv.keys()

    for value in column.values():
        assert value in column_sv.values()

    for key, value in column.items():
        assert key in column_sv.keys()
        assert value in column_sv.values()

    with pytest.raises(ResultAttributeError):
        column.wrong_attr
