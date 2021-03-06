from http import HTTPStatus
import json

from api.crud import CRUDSpot
from api.authentication import get_current_user
from spotapp import app
from tests import stubs, sample


async def override_dependency(anything: str = None):
    return {}

app.dependency_overrides[get_current_user] = override_dependency


def test_spot_get_by_id_ok(client, mocker):
    mocker.patch.object(CRUDSpot, "get_spot_by_id",
                        side_effect=stubs.get_spot_by_id_stub, autospec=True)
    response = client.get("/spots/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == sample.EXAMPLE_SPOT


def test_spot_get_by_id_422(client, mocker):
    mocker.patch.object(CRUDSpot, "get_spot_by_id",
                        side_effect=stubs.get_spot_by_id_empty_stub, autospec=True)
    response = client.get("/spots/wrong_data_type")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == sample.EXAMPLE_SPOT_422


def test_get_spots_ok(client, mocker):
    mocker.patch.object(CRUDSpot, "get_filtered_spots",
                        side_effect=stubs.get_spots_stub, autospec=True)
    response = client.get("/spots/filtered/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [sample.EXAMPLE_SPOT, sample.EXAMPLE_SPOT]


def test_create_spot_ok(client, mocker):
    mocker.patch.object(CRUDSpot, "add_spot",
                        side_effect=stubs.create_new_spot_stub, autospec=True)
    response = client.post("/spots/create/", json.dumps(sample.RAW_SPOT))
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == sample.EXAMPLE_SPOT


def test_delete_spot_ok(client, mocker):
    mocker.patch.object(CRUDSpot, "delete_spot",
                        side_effect=stubs.delete_spot_stub, autospec=True)
    response = client.delete("/spots/destroy/123")
    assert response.status_code == HTTPStatus.NO_CONTENT
