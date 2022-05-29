import pytest
from fastapi.testclient import TestClient

import spotapp


@pytest.fixture
def client():
    """Clien fixture"""

    with TestClient(spotapp.app) as client_fixture:
        yield client_fixture
