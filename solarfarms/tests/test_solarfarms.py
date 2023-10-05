import pytest
from fastapi.testclient import TestClient

from solarfarms.main import app


def test_get_farm_by_id():
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
    with TestClient(app) as client:
        response = client.get("/farms/{}".format(666))
        assert response.status_code == 404