import allure

from clients.authentication.authentication_schema import LoginResponseSchema
from tools.assertions.base import assert_equal, assert_is_true
from tools.logger import get_logger

logger = get_logger("AUTHENTICATION_ASSERTIONS")


@allure.step("Check login response")
def assert_login_response(response: LoginResponseSchema):
    """
    Checks the correctness of the response for successful authorization.

    :param response: Response object with authorization tokens.
    :raises AssertionError: If any of the conditions is not met.
    """
    logger.info("Check login response")

    assert_equal(response.token.token_type, "bearer", "token_type")
    assert_is_true(response.token.access_token, "access_token")
    assert_is_true(response.token.refresh_token, "refresh_token")
