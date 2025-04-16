from httpx import Response

from clients.api_client import APIClient
from clients.public_http_builder import get_public_http_client
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema, RefreshRequestSchema


class AuthenticationClient(APIClient):
    """
    Client for working with /api/v1/authentication
    """

    def login_api(self, request: LoginRequestSchema) -> Response:
        """
        This method performs user authentication.

        :param request: A LoginRequestSchema object containing email and password.
        :return: The server response as an httpx.Response object.
        """
        return self.post(
            "/api/v1/authentication/login",
            json=request.model_dump(by_alias=True)
        )

    def refresh_api(self, request: RefreshRequestSchema) -> Response:
        """
        This method refreshes the authorization token.

        :param request: A RefreshRequestSchema object containing refreshToken.
        :return: The server response as an httpx.Response object.
        """
        return self.post(
            "/api/v1/authentication/refresh",
            json=request.model_dump(by_alias=True)
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
