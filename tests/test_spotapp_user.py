from http import HTTPStatus
from api.crud import CRUDUser

from tests import stubs, sample


def test_user_get_by_id_ok(client, mocker):
    mocker.patch.object(CRUDUser, "get_user_by_id", side_effect=stubs.get_user_by_id_stub, autospec=True)
    response = client.get("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == sample.EXAMPLE_USER_GET
