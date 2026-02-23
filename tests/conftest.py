import copy
import pytest
from fastapi.testclient import TestClient
import httpx

import src.app as app_module
from src.app import app


@pytest.fixture(autouse=True)
def reset_activities():
    """Snapshot and restore the in-memory `activities` between tests."""
    original = copy.deepcopy(app_module.activities)
    try:
        yield
    finally:
        app_module.activities.clear()
        app_module.activities.update(original)


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
async def async_client():
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac
