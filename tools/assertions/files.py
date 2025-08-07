import allure

from clients.errors_schema import (
    InternalErrorResponseSchema,
    ValidationErrorResponseSchema,
    ValidationErrorSchema,
)
from clients.files.files_schema import (
    CreateFileRequestSchema,
    CreateFileResponseSchema,
    FileSchema,
    GetFileResponseSchema,
)
from config import settings
from tools.assertions.base import assert_equal
from tools.assertions.errors import (
    assert_internal_error_response,
    assert_validation_error_response,
)
from tools.logger import get_logger

logger = get_logger("FILES_ASSERTIONS")


@allure.step("Check create file response")
def assert_create_file_response(
    request: CreateFileRequestSchema,
    response: CreateFileResponseSchema,
):
    """
    Checks that the file creation response matches the request.

    :param request: The original file creation request.
    :param response: The API response with file data.
    :raises AssertionError: If at least one field does not match.
    """
    expected_url = f"{settings.http_client.client_url}static/{request.directory}/{request.filename}"

    logger.info("Check create file response")

    assert_equal(str(response.file.url), expected_url, "url")
    assert_equal(response.file.filename, request.filename, "filename")
    assert_equal(response.file.directory, request.directory, "directory")


@allure.step("Check file")
def assert_file(actual: FileSchema, expected: FileSchema):
    """
    Checks that the actual file data matches the expected data.

    :param actual: The actual file data.
    :param expected: The expected file data.
    :raises AssertionError: If at least one field does not match.
    """
    logger.info("Check file")

    assert_equal(actual=actual.id, expected=expected.id, name="id")
    assert_equal(actual=actual.url, expected=expected.url, name="url")
    assert_equal(actual=actual.filename, expected=expected.filename, name="filename")
    assert_equal(actual=actual.directory, expected=expected.directory, name="directory")


@allure.step("Check get file response")
def assert_get_file_response(
    get_file_response: GetFileResponseSchema, create_file_response: CreateFileResponseSchema
):
    """
    Checks that the response for getting a file matches the response for creating it.

    :param get_file_response: The API response when requesting file data.
    :param create_file_response: The API response when creating the file.
    :raises AssertionError: If the file data does not match.
    """
    logger.info("Check get file response")

    assert_file(get_file_response.file, create_file_response.file)


@allure.step("Check create file with empty filename response")
def assert_create_file_with_empty_filename_response(actual: ValidationErrorResponseSchema):
    """
    Checks that the response for creating a file with an empty filename matches the expected validation error.

    :param actual: The API response with the validation error to check.
    :raises AssertionError: If the actual response does not match the expected one.
    """
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="string_too_short",
                input="",
                context={"min_length": 1},
                message="String should have at least 1 character",
                location=["body", "filename"],
            )
        ]
    )
    logger.info("Check create file with empty filename response")

    assert_validation_error_response(actual, expected)


@allure.step("Check create file with empty directory response")
def assert_create_file_with_empty_directory_response(actual: ValidationErrorResponseSchema):
    """
    Checks that the response for creating a file with an empty directory value matches the expected validation error.

    :param actual: The API response with the validation error to check.
    :raises AssertionError: If the actual response does not match the expected one.
    """
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="string_too_short",
                input="",
                context={"min_length": 1},
                message="String should have at least 1 character",
                location=["body", "directory"],
            )
        ]
    )
    logger.info("Check create file with empty directory response")

    assert_validation_error_response(actual, expected)


@allure.step("Check file not found response")
def assert_file_not_found_response(actual: InternalErrorResponseSchema):
    """
    Checks that the response for a file not found error matches the expected internal error.

    :param actual: The API response with the internal error to check.
    :raises AssertionError: If the actual response does not match the expected "File not found" error.
    """
    expected = InternalErrorResponseSchema(details="File not found")  # type: ignore

    logger.info("Check file not found response")

    assert_internal_error_response(actual, expected)


@allure.step("Check get file with incorrect file id response")
def assert_get_file_with_incorrect_file_id_response(actual: ValidationErrorResponseSchema):
    """
    Checks that the response for getting a file with an incorrect file ID matches the expected validation error.

    :param actual: The API response with the validation error to check.
    :raises AssertionError: If the actual response does not match the expected one.
    """
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="uuid_parsing",
                input="incorrect-file-id",
                context={
                    "error": "invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1"
                },
                message="Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1",
                location=["path", "file_id"],
            )
        ]
    )
    logger.info("Check get file with incorrect file id response")

    assert_validation_error_response(actual, expected)
