import pytest
from pydantic import BaseModel

from config import settings

from clients.files.files_client import FilesClient, get_files_client
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema
from fixtures.users import UserFixture


class FileFixture(BaseModel):
    request: CreateFileRequestSchema
    response: CreateFileResponseSchema


@pytest.fixture
def files_client(function_user: UserFixture) -> FilesClient:
    """
    Creates a files client authenticated with the function-scoped user.
    :param function_user: The user fixture for the current test function.
    :return: An authenticated FilesClient instance.
    """
    return get_files_client(function_user.authentication_user)


@pytest.fixture
def function_file(files_client: FilesClient) -> FileFixture:
    """
    Creates a test file for the current test function.
    Uploads a predefined file using the function-scoped files client.
    :param files_client: Client for file operations, authenticated as the function user.
    :return: A FilesFixture containing the request and response data for the created file.
    """
    request = CreateFileRequestSchema(
        upload_file=settings.test_data.image_png_file
    )
    response = files_client.create_file(request=request)
    return FileFixture(request=request, response=response)
