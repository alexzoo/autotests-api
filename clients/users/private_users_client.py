from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient


class UpdateUserRequestDict(TypedDict):
    """
    Description of the structure of the request to update a user.
    """
    email: str | None
    lastName: str | None
    firstName: str | None
    middleName: str | None


class PrivateUsersClient(APIClient):
    """
    Client for working with /api/v1/users
    """

    def get_user_me_api(self) -> Response:
        """
        Method to retrieve information about the current user.

        :return: The server response as an httpx.Response object.
        """
        return self.get("/api/v1/users/me")

    def get_user_api(self, user_id: str) -> Response:
        """
        Method to retrieve a user by their identifier.

        :param user_id: The identifier of the user.
        :return: The server response as an httpx.Response object.
        """
        return self.get(f"/api/v1/users/{user_id}")

    def update_user_api(self, user_id: str, request: UpdateUserRequestDict) -> Response:
        """
        Method to update a user by their identifier.

        :param user_id: The identifier of the user.
        :param request: Dictionary with user data to update.
        :return: The server response as an httpx.Response object.
        """
        return self.patch(f"/api/v1/users/{user_id}", json=request)

    def delete_user_api(self, user_id: str) -> Response:
        """
        Method to delete a user by their identifier.

        :param user_id: The identifier of the user.
        :return: The server response as an httpx.Response object.
        """
        return self.delete(f"/api/v1/users/{user_id}")
