import json

from pkg_resources import resource_string
import pytest


@pytest.fixture
def cineplex_api_response():
    yield json.loads(resource_string("tests", f"test_data/cineplex_api.txt").decode('utf-8'))

