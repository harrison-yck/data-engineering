import json

from pkg_resources import resource_string
import fakeredis as fakeredis
import pytest


@pytest.fixture
def redis_mock():
    yield fakeredis.FakeStrictRedis()


@pytest.fixture
def cineplex_api_response():
    yield json.loads(resource_string("tests", f"test_data/cineplex_api.txt").decode('utf-8'))


@pytest.fixture
def redis_config():
    yield {
        "host": "redis",
        "port": "6379",
        "db": 0
    }

