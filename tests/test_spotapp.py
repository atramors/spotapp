from http import HTTPStatus


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == HTTPStatus.OK
