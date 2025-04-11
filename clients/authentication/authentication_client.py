from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient


class LoginRequestDict(TypedDict):
    """
    Description of the authentication request structure.
    """
    email: str
    password: str


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
