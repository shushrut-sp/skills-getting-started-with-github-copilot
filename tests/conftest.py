import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def activities_snapshot():
    """Snapshot and restore the module-level `activities` dict around each test.

    This keeps tests isolated (AAA pattern relies on a known starting state).
    """
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)
