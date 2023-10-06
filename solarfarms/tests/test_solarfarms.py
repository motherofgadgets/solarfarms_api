import pytest
from fastapi.testclient import TestClient

from solarfarms.main import app


def test_get_farm_by_id():
    """
    Tests that when given a valid farm ID, the app returns the correct Farm object.
    """
    with TestClient(app) as client:
        response = client.get("/farms/{}".format(150))
        assert response.status_code == 200
        assert response.json() == {
            "id": 150,
            "name": "Ashby I and 2 Solar",
            "capacity_kw": 1848.0,
            "address": "1180 Ashby State Road",
            "city": "Fitchburg",
            "state": "MA",
            "zip": "02132",
        }


def test_get_farm_by_id_not_found():
    """
    Tests that when given a farm ID that does not match any in the database, a 404 error is thrown
    """
    with TestClient(app) as client:
        response = client.get("/farms/{}".format(666))
        assert response.status_code == 404


def test_get_farms_by_state():
    """
    Tests that app correctly filters by state
    """
    with TestClient(app) as client:
        response = client.get("/farms/?state=MA")
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 51,
                "name": "Nexamp Peak",
                "capacity_kw": 1750.0,
                "address": "271 Brodie Mountain Road",
                "city": "Hancock",
                "state": "MA",
                "zip": "01237",
            },
            {
                "id": 56,
                "name": "Avon Solar",
                "capacity_kw": 990.0,
                "address": "55 Murphy Drive",
                "city": "Avon",
                "state": "MA",
                "zip": "02322",
            },
            {
                "id": 150,
                "name": "Ashby I and 2 Solar",
                "capacity_kw": 1848.0,
                "address": "1180 Ashby State Road",
                "city": "Fitchburg",
                "state": "MA",
                "zip": "02132",
            },
        ]


def test_get_farm_by_state_not_found():
    """
    Tests that app returns a 404 error when no Farms have the given state value
    """
    with TestClient(app) as client:
        response = client.get("/farms/?state=XX")
        assert response.status_code == 404


def test_get_farms_btw_max_and_min_capacity():
    """
    Tests that app correctly filters Farms with capacity values in the given range
    """
    with TestClient(app) as client:
        response = client.get("/farms/?min_capacity=500&max_capacity=1000")
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 33,
                "name": "Harrison Solar",
                "capacity_kw": 500.0,
                "address": "1 Westchester Park Drive",
                "city": "Harrison",
                "state": "NY",
                "zip": "10604",
            },
            {
                "id": 56,
                "name": "Avon Solar",
                "capacity_kw": 990.0,
                "address": "55 Murphy Drive",
                "city": "Avon",
                "state": "MA",
                "zip": "02322",
            },
            {
                "id": 176,
                "name": "Coventry Solar",
                "capacity_kw": 750.0,
                "address": "0 Lewis Farm Road",
                "city": "Coventry",
                "state": "RI",
                "zip": "02827",
            },
        ]


def test_get_farms_min_capacity_only():
    """
    Tests that app correctly filters Farms when only a minimum value is provided.
    """
    with TestClient(app) as client:
        response = client.get("/farms/?min_capacity=1500")
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 51,
                "name": "Nexamp Peak",
                "capacity_kw": 1750.0,
                "address": "271 Brodie Mountain Road",
                "city": "Hancock",
                "state": "MA",
                "zip": "01237",
            },
            {
                "id": 150,
                "name": "Ashby I and 2 Solar",
                "capacity_kw": 1848.0,
                "address": "1180 Ashby State Road",
                "city": "Fitchburg",
                "state": "MA",
                "zip": "02132",
            },
        ]


def test_get_farms_max_capacity_only():
    """
    Tests that app correctly filters Farms when only a maximum value is provided.
    """
    with TestClient(app) as client:
        response = client.get("/farms/?max_capacity=500")
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 31,
                "name": "Factory Street Solar",
                "capacity_kw": 300.0,
                "address": "100 Factory Street",
                "city": "West Warwick",
                "state": "RI",
                "zip": "02893",
            },
            {
                "id": 33,
                "name": "Harrison Solar",
                "capacity_kw": 500.0,
                "address": "1 Westchester Park Drive",
                "city": "Harrison",
                "state": "NY",
                "zip": "10604",
            },
            {
                "id": 52,
                "name": "Richmond Solar",
                "capacity_kw": 499.0,
                "address": "Lot 44-1 Stilson Road",
                "city": "Richmond",
                "state": "RI",
                "zip": "02898",
            },
        ]


def test_get_farms_btw_max_and_min_capacity_none_found():
    """
    Tests that a 404 Error is returned if no Farms have values in the specified range
    """
    with TestClient(app) as client:
        response = client.get("/farms/?min_capacity=2000&max_capacity=3000")
        assert response.status_code == 404


def test_get_farms_btw_max_and_min_capacity_min_gt_max():
    """
    Tests that a 400 error is returned if the min_capacity value is higher than max_capacity
    """
    with TestClient(app) as client:
        response = client.get("/farms/?min_capacity=1000&max_capacity=500")
        assert response.status_code == 400


def test_get_farm_max_month():
    """
    Tests that the app correctly calculates and returns the month with the most energy generated.
    """
    with TestClient(app) as client:
        response = client.get("/farms/31/maxmonth")
        assert response.status_code == 200
        assert response.json() == {
            "year": 2018,
            "month": 6,
            "month_total": 576964.4263453905,
        }


def test_get_farm_max_month_farm_not_found():
    """
    Tests that a 404 error is thrown if given a farm ID that does not match any in the database
    """
    with TestClient(app) as client:
        response = client.get("/farms/99/maxmonth")
        assert response.status_code == 404
