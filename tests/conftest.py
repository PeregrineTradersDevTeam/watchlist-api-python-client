import pytest
import responses


@pytest.fixture
def mocked_response():
    """A pytest fixture to mock the behaviour of a server sending back a response."""
    with responses.RequestsMock() as mocked_response:
        yield mocked_response
