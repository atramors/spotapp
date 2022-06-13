from http import HTTPStatus
from api.crud import CRUDUser

from tests import stubs, sample


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == HTTPStatus.OK


def test_user_get_by_id_ok(client, mocker):
    mocker.patch.object(CRUDUser, "get_user_by_id", side_effect=stubs.get_user_by_id_stub, autospec=True)
    response = client.get("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == sample.EXAMPLE_USER_GET


def test_user_get_by_id_422(client, mocker):
    mocker.patch.object(CRUDUser, "get_user_by_id", side_effect=stubs.get_user_by_id_empty_stub, autospec=True)
    response = client.get("/users/wrong_data_type")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == sample.EXAMPLE_USER_422


def test_user_get_all_ok(client, mocker):
    mocker.patch.object(CRUDUser, "get_all_users", side_effect=stubs.get_all_users_stub, autospec=True)
    response = client.get("/users/all/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [sample.EXAMPLE_USER_GET, sample.EXAMPLE_USER_GET]
