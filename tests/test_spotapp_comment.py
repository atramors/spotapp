from http import HTTPStatus
import json

from api.crud import CRUDComment
from tests import stubs, sample


def test_comment_get_by_id_ok(client, mocker):
    mocker.patch.object(CRUDComment, "get_comment_by_id",
                        side_effect=stubs.get_comment_by_id_stub, autospec=True)
    response = client.get("/comments/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == sample.EXAMPLE_COMMENT


def test_comment_get_by_id_422(client, mocker):
    mocker.patch.object(CRUDComment, "get_comment_by_id",
                        side_effect=stubs.get_comment_by_id_empty_stub, autospec=True)
    response = client.get("/comments/wrong_data_type")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == sample.EXAMPLE_COMMENT_422


# def test_create_comment_ok(client, mocker):
#     mocker.patch.object(CRUDComment, "add_comment",
#                         side_effect=stubs.create_new_comment_stub, autospec=True)
#     response = client.post("/comments/create_comment/", json.dumps(sample.RAW_SPOT))
#     assert response.status_code == HTTPStatus.CREATED
#     assert response.json() == sample.EXAMPLE_SPOT


# def test_delete_comment_ok(client, mocker):
#     mocker.patch.object(CRUDSpot, "delete_comment",
#                         side_effect=stubs.delete_comment_stub, autospec=True)
#     response = client.delete("/comments/destroy_comment/123")
#     assert response.status_code == HTTPStatus.NO_CONTENT
#     assert response.json() == sample.DELETED_SPOT
