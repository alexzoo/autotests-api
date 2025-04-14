from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient


class CreateFileRequestDict(TypedDict):
    """
    Description of the request structure for creating a file.
    """
    filename: str
    directory: str
    upload_file: str


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
