import pytest
from fastapi.testclient import TestClient

from solarfarms.main import app


client = TestClient(app)


def test_get_farm_by_id():
    test_id = 1
    response = client.get("/farms/{}".format(test_id))
    assert response.status_code == 200
    assert response.json() == {
        "farm": test_id
    }
