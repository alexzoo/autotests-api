import allure
from httpx import Response

from clients.api_client import APIClient
from clients.authentication.authentication_schema import (
    LoginRequestSchema,
    LoginResponseSchema,
    RefreshRequestSchema,
)
from clients.public_http_builder import get_public_http_client
from tools.routes import APIRoutes


class AuthenticationClient(APIClient):
    """
    Client for working with /api/v1/authentication
    """

    @allure.step("Authenticate user")
    def login_api(self, request: LoginRequestSchema) -> Response:
        """
        This method performs user authentication.

        :param request: A LoginRequestSchema object containing email and password.
        :return: The server response as an httpx.Response object.
        """
        return self.post(
            f"{APIRoutes.AUTHENTICATION}/login", json=request.model_dump(by_alias=True)
        )

    @allure.step("Refresh authentication token")
    def refresh_api(self, request: RefreshRequestSchema) -> Response:
        """
        This method refreshes the authorization token.

        :param request: A RefreshRequestSchema object containing refreshToken.
        :return: The server response as an httpx.Response object.
        """
        return self.post(
            f"{APIRoutes.AUTHENTICATION}/refresh", json=request.model_dump(by_alias=True)
        )

    def login(self, request: LoginRequestSchema) -> LoginResponseSchema:
        """
        Performs user authentication and returns the parsed JSON response.

        This is a convenience method that calls login_api and automatically converts
        the response to a LoginResponseSchema.

        :param request: A LoginRequestSchema object containing email and password.
        :return: The parsed response containing authentication tokens.
        """
        response = self.login_api(request)
        return LoginResponseSchema.model_validate_json(response.text)


def get_authentication_client() -> AuthenticationClient:
    """
    Creates an instance of AuthenticationClient with a pre-configured HTTP client.

    :return: Ready-to-use AuthenticationClient.
    """
    return AuthenticationClient(client=get_public_http_client())
