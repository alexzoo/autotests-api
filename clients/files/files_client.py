from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient
from clients.private_http_builder import AuthenticationUserDict, get_private_http_client


class File(TypedDict):
    """
    Description of the file structure.
    """
    id: str
    url: str
    filename: str
    directory: str


class CreateFileRequestDict(TypedDict):
    """
    Description of the request structure for creating a file.
    """
    filename: str
    directory: str
    upload_file: str


class CreateFileResponseDict(TypedDict):
    """
    Description of the response structure for creating a file.
    """
    file: File


class FilesClient(APIClient):
    """
    Client for working with /api/v1/files
    """

    def get_file_api(self, file_id: str) -> Response:
        """
        Method to retrieve a file by its identifier.

        :param file_id: The identifier of the file.
        :return: The server response as an httpx.Response object.
        """
        return self.get(f"/api/v1/files/{file_id}")

    def create_file_api(self, request: CreateFileRequestDict) -> Response:
        """
        Method to create a new file.

        :param request: Dictionary with file data including filename, directory and path to the file to upload.
        :return: The server response as an httpx.Response object.
        """
        return self.post(
            "/api/v1/files",
            data=request,
            files={"upload_file": open(request['upload_file'], 'rb')}
        )

    def delete_file_api(self, file_id: str) -> Response:
        """
        Method to delete a file by its identifier.

        :param file_id: The identifier of the file.
        :return: The server response as an httpx.Response object.
        """
        return self.delete(f"/api/v1/files/{file_id}")

    def create_file(self, request: CreateFileRequestDict) -> CreateFileResponseDict:
        """
        Method to create a new file and return the response data.

        :param request: Dictionary with file data including filename, directory and path to the file to upload.
        :return: The file creation response data as a dictionary.
        """
        response = self.create_file_api(request)
        return response.json()


def get_files_client(user: AuthenticationUserDict) -> FilesClient:
    """
    Function creates an instance of FilesClient with a pre-configured HTTP client.

    :param user: User authentication data.
    :return: Ready-to-use FilesClient.
    """
    return FilesClient(client=get_private_http_client(user))
