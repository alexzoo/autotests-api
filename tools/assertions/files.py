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
from tools.assertions.base import assert_equal
from tools.assertions.errors import (
    assert_internal_error_response,
    assert_validation_error_response,
)


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
    expected_url = f"http://localhost:8000/static/{request.directory}/{request.filename}"

    assert_equal(str(response.file.url), expected_url, "url")
    assert_equal(response.file.filename, request.filename, "filename")
    assert_equal(response.file.directory, request.directory, "directory")


def assert_file(actual: FileSchema, expected: FileSchema):
    """
    Checks that the actual file data matches the expected data.

    :param actual: The actual file data.
    :param expected: The expected file data.
    :raises AssertionError: If at least one field does not match.
    """
    assert_equal(actual=actual.id, expected=expected.id, name="id")
    assert_equal(actual=actual.url, expected=expected.url, name="url")
    assert_equal(actual=actual.filename, expected=expected.filename, name="filename")
    assert_equal(actual=actual.directory, expected=expected.directory, name="directory")


def assert_get_file_response(
    get_file_response: GetFileResponseSchema, create_file_response: CreateFileResponseSchema
):
    """
    Checks that the response for getting a file matches the response for creating it.

    :param get_file_response: The API response when requesting file data.
    :param create_file_response: The API response when creating the file.
    :raises AssertionError: If the file data does not match.
    """
    assert_file(get_file_response.file, create_file_response.file)


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
    assert_validation_error_response(actual, expected)


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
    assert_validation_error_response(actual, expected)


def assert_file_not_found_response(actual: InternalErrorResponseSchema):
    """
    Checks that the response for a file not found error matches the expected internal error.

    :param actual: The API response with the internal error to check.
    :raises AssertionError: If the actual response does not match the expected "File not found" error.
    """
    expected = InternalErrorResponseSchema(details="File not found")  # type: ignore
    assert_internal_error_response(actual, expected)


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
    assert_validation_error_response(actual, expected)
