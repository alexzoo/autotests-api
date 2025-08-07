import allure

from clients.users.users_schema import (
    CreateUserRequestSchema,
    CreateUserResponseSchema,
    GetUserResponseSchema,
    UserSchema,
)
from tools.assertions.base import assert_equal
from tools.logger import get_logger

logger = get_logger("USERS_ASSERTIONS")


@allure.step("Check create user response")
def assert_create_user_response(request: CreateUserRequestSchema, response: CreateUserResponseSchema):
    """
    Verifies that the user creation response matches the request.

    :param request: Original user creation request.
    :param response: API response with user data.
    :raises AssertionError: If any field doesn't match.
    """
    logger.info("Check create user response")

    assert_equal(response.user.email, request.email, "email")
    assert_equal(response.user.last_name, request.last_name, "last_name")
    assert_equal(response.user.first_name, request.first_name, "first_name")
    assert_equal(response.user.middle_name, request.middle_name, "middle_name")


@allure.step("Check user")
def assert_user(actual: UserSchema, expected: UserSchema):
    """
    Assert that two UserSchema objects have the same properties.
    Compares the id, email, first_name, last_name, and middle_name fields
    of the actual and expected UserSchema objects.
    :param actual: The actual UserSchema object
    :param expected: The expected UserSchema object
    :raises AssertionError: If any of the comparisons fail
    """
    logger.info("Check user")

    assert_equal(actual=actual.id, expected=expected.id, name="id")
    assert_equal(actual=actual.email, expected=expected.email, name="email")
    assert_equal(actual=actual.first_name, expected=expected.first_name, name="first_name")
    assert_equal(actual=actual.last_name, expected=expected.last_name, name="last_name")
    assert_equal(actual=actual.middle_name, expected=expected.middle_name, name="middle_name")


@allure.step("Check get user response")
def assert_get_user_response(
    get_user_response: GetUserResponseSchema, create_user_response: CreateUserResponseSchema
):
    """
    Verifies that the user from get user response matches the user from create user response.

    :param get_user_response: Response from get user endpoint
    :param create_user_response: Response from create user endpoint
    :raises AssertionError: If any user field doesn't match
    """
    logger.info("Check get user response")
    assert_user(actual=get_user_response.user, expected=create_user_response.user)
