import pytest

@pytest.fixture
def non_mocked_hosts() -> list:
    return ["testserver"]