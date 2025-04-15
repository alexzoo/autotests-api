from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient
from clients.public_http_builder import get_public_http_client


class User(TypedDict):
    """
    Description of the user structure.
    """
    id: str
    email: str
    lastName: str
    firstName: str
    middleName: str


class CreateUserRequestDict(TypedDict):
    """
    Description of the user creation request structure.
    """
    email: str
    password: str
    lastName: str
    firstName: str
    middleName: str


class CreateUserResponseDict(TypedDict):
    """
    Description of the user creation response structure.
    """
    user: User


class PublicUsersClient(APIClient):
    """
    Client for working with /api/v1/users
    """

    def create_user_api(self, request: CreateUserRequestDict) -> Response:
        """
        This method sends a request to create a new user.

        :param request: A dictionary containing user data (email, password, lastName, firstName, middleName).
        :return: The server response as an httpx.Response object.
        """
        return self.post("/api/v1/users", json=request)

    def create_user(self, request: CreateUserRequestDict) -> CreateUserResponseDict:
        """
        This method creates a new user and returns the parsed response.

        :param request: A dictionary containing user data (email, password, lastName, firstName, middleName).
        :return: A typed dictionary containing the created user information.
        """
        response = self.create_user_api(request)
        return response.json()


def get_public_users_client() -> PublicUsersClient:
    """
    This function creates an instance of PublicUsersClient with a pre-configured HTTP client.

    :return: A ready-to-use PublicUsersClient.
    """
    return PublicUsersClient(client=get_public_http_client())
