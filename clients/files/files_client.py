import allure
from httpx import Response

from clients.api_client import APIClient
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema
from clients.private_http_builder import AuthenticationUserSchema, get_private_http_client
from tools.routes import APIRoutes


class FilesClient(APIClient):
    """
    Client for working with /api/v1/files
    """

    @allure.step("Get file by id {file_id}")
    def get_file_api(self, file_id: str) -> Response:
        """
        Method to retrieve a file by its identifier.

        :param file_id: The identifier of the file.
        :return: The server response as an httpx.Response object.
        """
        return self.get(f"{APIRoutes.FILES}/{file_id}")

    @allure.step("Create file")
    def create_file_api(self, request: CreateFileRequestSchema) -> Response:
        """
        Method to create a new file.

        :param request: CreateFileRequestSchema with file data including filename, directory and
        path to the file to upload.
        :return: The server response as an httpx.Response object.
        """
        return self.post(
            url=APIRoutes.FILES,
            data=request.model_dump(by_alias=True, exclude={"upload_file"}),
            files={"upload_file": request.upload_file.read_bytes()},
        )

    @allure.step("Delete file by id {file_id}")
    def delete_file_api(self, file_id: str) -> Response:
        """
        Method to delete a file by its identifier.

        :param file_id: The identifier of the file.
        :return: The server response as an httpx.Response object.
        """
        return self.delete(f"{APIRoutes.FILES}/{file_id}")

    def create_file(self, request: CreateFileRequestSchema) -> CreateFileResponseSchema:
        """
        Method to create a new file and return the response data.

        :param request: CreateFileRequestSchema with file data including filename, directory and
        path to the file to upload.
        :return: CreateFileResponseSchema with data of the created file.
        """
        response = self.create_file_api(request)
        return CreateFileResponseSchema.model_validate_json(response.text)


def get_files_client(user: AuthenticationUserSchema) -> FilesClient:
    """
    Function creates an instance of FilesClient with a pre-configured HTTP client.

    :param user: User authentication data.
    :return: Ready-to-use FilesClient.
    """
    return FilesClient(client=get_private_http_client(user))
