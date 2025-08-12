from typing import Any, Sized

import allure

from tools.logger import get_logger

logger = get_logger("BASE_ASSERTIONS")


@allure.step("Check that response status code equals to {expected}")
def assert_status_code(actual: int, expected: int):
    """
    Verifies that the actual response status code matches the expected one.

    :param actual: The actual response status code.
    :param expected: The expected status code.
    :raises AssertionError: If the status codes do not match.
    """
    logger.info(f"Check that response status code equals to {expected}")

    assert actual == expected, (
        f"Incorrect response status code. Expected status code: {expected}. Actual status code: {actual}"
    )


@allure.step("Check that {name} equals to {expected}")
def assert_equal(actual: Any, expected: Any, name: str):
    """
    Verifies that the actual value matches the expected one.

    :param actual: The actual value.
    :param expected: The expected value.
    :param name: The name of the value being verified.
    :raises AssertionError: If the actual value does not match the expected one.
    """
    logger.info(f'Check that "{name}" equals to {expected}')

    assert actual == expected, (
        f'Incorrect value: "{name}". Expected value: {expected}. Actual value: {actual}'
    )


@allure.step("Check that {name} is true")
def assert_is_true(actual: Any, name: str):
    """
    Verifies that the actual value is true.

    :param actual: The actual value.
    :param name: The name of the value being verified.
    :raises AssertionError: If the actual value is false.
    """
    logger.info(f'Check that "{name}" is true')

    assert actual, f'Incorrect value: "{name}". Expected true value but got: {actual}'


def assert_length(actual: Sized, expected: Sized, name: str):
    """
    Verifies that the lengths of two objects match.

    :param actual: The actual object.
    :param expected: The expected object.
    :param name: The name of the object being verified.
    :raises AssertionError: If the lengths do not match.
    """
    with allure.step(f"Check that length of {name} equals to {len(expected)}"):
        logger.info(f'Check that length of "{name}" equals to {len(expected)}')

        assert len(actual) == len(expected), (
            f'Incorrect object length: "{name}". '
            f"Expected length: {len(expected)}. "
            f"Actual length: {len(actual)}"
        )
