import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient

import spotapp
from api.models import Base
from api.db import async_engine


@pytest.fixture
def client():
    """Client fixture"""

    with TestClient(spotapp.app) as client_fixture:
        yield client_fixture


@pytest.fixture
async def async_client():
    """Async client fixture"""

    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with AsyncClient(app=spotapp.app, base_url="http://test") as client_fixture:
        yield client_fixture

    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
