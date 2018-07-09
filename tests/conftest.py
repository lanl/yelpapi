import pytest
from faker import Faker
from requests_mock import Mocker


@pytest.fixture(autouse=True)
def mock_request():
    with Mocker(case_sensitive=True) as mock:
        yield mock


@pytest.fixture
def faker():
    return Faker()
