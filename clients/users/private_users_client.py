import allure
from httpx import Response

from clients.api_client import APIClient
from clients.private_http_builder import AuthenticationUserSchema, get_private_http_client
from clients.users.users_schema import GetUserResponseSchema, UpdateUserRequestSchema


class PrivateUsersClient(APIClient):
    """
    Client for working with /api/v1/users
    """

    @allure.step("Get user me")
    def get_user_me_api(self) -> Response:
        """
        Method to retrieve information about the current user.

        :return: The server response as an httpx.Response object.
        """
        return self.get("/api/v1/users/me")

    @allure.step("Get user by id {user_id}")
    def get_user_api(self, user_id: str) -> Response:
        """
        Method to retrieve a user by their identifier.

        :param user_id: The identifier of the user.
        :return: The server response as an httpx.Response object.
        """
        return self.get(f"/api/v1/users/{user_id}")

    @allure.step("Update user by id {user_id}")
    def update_user_api(self, user_id: str, request: UpdateUserRequestSchema) -> Response:
        """
        Method to update a user by their identifier.

        :param user_id: The identifier of the user.
        :param request: UpdateUserRequestSchema with user data to update.
        :return: The server response as an httpx.Response object.
        """
        return self.patch(f"/api/v1/users/{user_id}", json=request.model_dump(by_alias=True))

    @allure.step("Delete user by id {user_id}")
    def delete_user_api(self, user_id: str) -> Response:
        """
        Method to delete a user by their identifier.

        :param user_id: The identifier of the user.
        :return: The server response as an httpx.Response object.
        """
        return self.delete(f"/api/v1/users/{user_id}")

    def get_user(self, user_id: str) -> GetUserResponseSchema:
        """
        Method to retrieve a user by their identifier.

        :param user_id: The identifier of the user.
        :return: GetUserResponseSchema containing the user information.
        """
        response = self.get_user_api(user_id)
        return GetUserResponseSchema.model_validate_json(response.text)


def get_private_users_client(user: AuthenticationUserSchema) -> PrivateUsersClient:
    """
    Function that creates an instance of PrivateUsersClient with a preconfigured HTTP client.

    :param user: User authentication details.
    :return: A ready-to-use PrivateUsersClient.
    """
    return PrivateUsersClient(client=get_private_http_client(user))
