import allure

from clients.errors_schema import (
    InternalErrorResponseSchema,
    ValidationErrorResponseSchema,
    ValidationErrorSchema,
)
from tools.assertions.base import assert_equal, assert_length


@allure.step("Check validation error")
def assert_validation_error(actual: ValidationErrorSchema, expected: ValidationErrorSchema):
    """
    Checks that the validation error object matches the expected value.

    :param actual: The actual error.
    :param expected: The expected error.
    :raises AssertionError: If the field values do not match.
    """
    assert_equal(actual.type, expected.type, "type")
    assert_equal(actual.input, expected.input, "input")
    assert_equal(actual.context, expected.context, "context")
    assert_equal(actual.message, expected.message, "message")
    assert_equal(actual.location, expected.location, "location")


@allure.step("Check validation error response")
def assert_validation_error_response(
    actual: ValidationErrorResponseSchema,
    expected: ValidationErrorResponseSchema,
):
    """
    Checks that the API response object with validation errors (`ValidationErrorResponseSchema`)
    matches the expected value.

    :param actual: The actual API response.
    :param expected: The expected API response.
    :raises AssertionError: If the field values do not match.
    """
    assert_length(actual.details, expected.details, "details")

    for index, detail in enumerate(expected.details):
        assert_validation_error(actual.details[index], detail)


@allure.step("Check internal error response")
def assert_internal_error_response(
    actual: InternalErrorResponseSchema, expected: InternalErrorResponseSchema
):
    """
    Checks that the API response object with an internal error (`InternalErrorResponseSchema`)
    matches the expected value. For example, a 404 (File not found) error.

    :param actual: The actual API response.
    :param expected: The expected API response.
    :raises AssertionError: If the field values do not match.
    """
    assert_equal(actual.details, expected.details, "details")
