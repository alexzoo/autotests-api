import pytest

from clients.authentication.authentication_client import (
    AuthenticationClient,
    get_authentication_client,
)


@pytest.fixture
def authentication_client() -> AuthenticationClient:
    """
    Provides an instance of the authentication client.
    Creates and returns a new authentication client for API tests.
    :return: An instance of AuthenticationClient
    """
    return get_authentication_client()
