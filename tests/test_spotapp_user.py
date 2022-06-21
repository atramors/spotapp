from http import HTTPStatus
import json

from api.crud import CRUDUser
from tests import stubs, sample


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == HTTPStatus.OK


def test_user_get_by_id_ok(client, mocker):
    mocker.patch.object(CRUDUser, "get_user_by_id",
                        side_effect=stubs.get_user_by_id_stub, autospec=True)
    response = client.get("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == sample.EXAMPLE_USER


def test_user_get_by_id_422(client, mocker):
    mocker.patch.object(CRUDUser, "get_user_by_id",
                        side_effect=stubs.get_user_by_id_empty_stub, autospec=True)
    response = client.get("/users/wrong_data_type")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == sample.EXAMPLE_USER_422


def test_user_get_all_ok(client, mocker):
    mocker.patch.object(CRUDUser, "get_all_users",
                        side_effect=stubs.get_all_users_stub, autospec=True)
    response = client.get("/users/all/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [sample.EXAMPLE_USER, sample.EXAMPLE_USER]


def test_create_user_ok(client, mocker):
    mocker.patch.object(CRUDUser, "add_user",
                        side_effect=stubs.create_new_user_stub, autospec=True)
    response = client.post("/users/create/", json.dumps(sample.RAW_USER))
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == sample.EXAMPLE_NEW_USER_ADD


def test_delete_user_ok(client, mocker):
    mocker.patch.object(CRUDUser, "delete_user",
                        side_effect=stubs.delete_user_stub, autospec=True)
    response = client.delete("/users/destroy/123")
    assert response.status_code == HTTPStatus.NO_CONTENT
