from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient
from clients.public_http_builder import get_public_http_client


class Token(TypedDict):
    """
    Description of the authentication tokens structure.
    """
    tokenType: str
    accessToken: str
    refreshToken: str


class LoginRequestDict(TypedDict):
    """
    Description of the authentication request structure.
    """
    email: str
    password: str


class LoginResponseDict(TypedDict):
    """
    Description of the authentication response structure.
    """
    token: Token


class RefreshRequestDict(TypedDict):
    """
    Description of the request structure for token refresh.
    """
    refreshToken: str


class AuthenticationClient(APIClient):
    """
    Client for working with /api/v1/authentication
    """

    def login_api(self, request: LoginRequestDict) -> Response:
        """
        This method performs user authentication.

        :param request: A dictionary with email and password.
        :return: The server response as an httpx.Response object.
        """
        return self.post("/api/v1/authentication/login", json=request)

    def refresh_api(self, request: RefreshRequestDict) -> Response:
        """
        This method refreshes the authorization token.

        :param request: A dictionary with refreshToken.
        :return: The server response as an httpx.Response object.
        """
        return self.post("/api/v1/authentication/refresh", json=request)

    def login(self, request: LoginRequestDict) -> LoginResponseDict:
        response = self.login_api(request)
        return response.json()


def get_authentication_client() -> AuthenticationClient:
    """
    Creates an instance of AuthenticationClient with a pre-configured HTTP client.

    :return: Ready-to-use AuthenticationClient.
    """
    return AuthenticationClient(client=get_public_http_client())
