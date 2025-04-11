from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient


class UserCreateRequestDict(TypedDict):
    """
    Description of the user creation request structure.
    """
    email: str
    password: str
    lastName: str
    firstName: str
    middleName: str


class PublicUsersClient(APIClient):
    """
    Client for working with /api/v1/users
    """
    def create_user_api(self, request: UserCreateRequestDict) -> Response:
        """
        This method sends a request to create a new user.

        :param request: A dictionary containing user data (email, password, lastName, firstName, middleName).
        :return: The server response as an httpx.Response object.
        """
        return self.post("/api/v1/users", json=request)
