from httpx import Response

from clients.api_client import APIClient
from clients.public_http_builder import get_public_http_client
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema
import allure

class PublicUsersClient(APIClient):
    """
    Client for working with /api/v1/users
    """

    @allure.step("Create user")
    def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        """
        This method sends a request to create a new user.

        :param request: A CreateUserRequestSchema object containing user data.
        :return: The server response as an httpx.Response object.
        """
        return self.post("/api/v1/users", json=request.model_dump(by_alias=True))

    def create_user(self, request: CreateUserRequestSchema) -> CreateUserResponseSchema:
        """
        This method creates a new user and returns the parsed response.

        :param request: A CreateUserRequestSchema object containing user data.
        :return: CreateUserResponseSchema object containing the created user information.
        """
        response = self.create_user_api(request)
        return CreateUserResponseSchema.model_validate_json(response.text)


def get_public_users_client() -> PublicUsersClient:
    """
    This function creates an instance of PublicUsersClient with a pre-configured HTTP client.

    :return: A ready-to-use PublicUsersClient.
    """
    return PublicUsersClient(client=get_public_http_client())
