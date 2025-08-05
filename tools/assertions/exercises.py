from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
    ExerciseSchema,
    GetExerciseResponseSchema,
    GetExercisesResponseSchema,
    UpdateExerciseRequestSchema,
    UpdateExerciseResponseSchema,
)
from tools.assertions.base import assert_equal, assert_length
from tools.assertions.errors import assert_internal_error_response

import allure


@allure.step("Check create exercise response")
def assert_create_exercise_response(
    request: CreateExerciseRequestSchema, response: CreateExerciseResponseSchema
):
    """
    Checks that the exercise creation response corresponds to the data from the request.

    :param request: The original request to create the exercise.
    :param response: The API response with the created exercise data.
    :raises AssertionError: If at least one field does not match.
    """
    assert_equal(actual=response.exercise.title, expected=request.title, name="title")
    assert_equal(actual=response.exercise.course_id, expected=request.course_id, name="course_id")
    assert_equal(actual=response.exercise.max_score, expected=request.max_score, name="max_score")
    assert_equal(actual=response.exercise.min_score, expected=request.min_score, name="min_score")
    assert_equal(
        actual=response.exercise.order_index, expected=request.order_index, name="order_index"
    )
    assert_equal(
        actual=response.exercise.description, expected=request.description, name="description"
    )
    assert_equal(
        actual=response.exercise.estimated_time,
        expected=request.estimated_time,
        name="estimated_time",
    )

@allure.step("Check exercise")
def assert_exercise(actual: ExerciseSchema, expected: ExerciseSchema):
    """
    Checks that the actual exercise matches the expected exercise.

    :param actual: The actual ExerciseSchema object to verify.
    :param expected: The expected ExerciseSchema object to compare against.
    :raises AssertionError: If at least one field does not match.
    """
    assert_equal(actual=actual.id, expected=expected.id, name="id")
    assert_equal(actual=actual.title, expected=expected.title, name="title")
    assert_equal(actual=actual.course_id, expected=expected.course_id, name="course_id")
    assert_equal(actual=actual.max_score, expected=expected.max_score, name="max_score")
    assert_equal(actual=actual.min_score, expected=expected.min_score, name="min_score")
    assert_equal(actual=actual.order_index, expected=expected.order_index, name="order_index")
    assert_equal(actual=actual.description, expected=expected.description, name="description")
    assert_equal(
        actual=actual.estimated_time, expected=expected.estimated_time, name="estimated_time"
    )

@allure.step("Check get exercise response")
def assert_get_exercise_response(
    get_exercise_response: GetExerciseResponseSchema,
    create_exercise_response: CreateExerciseResponseSchema,
):
    """
    Checks that the response for getting an exercise matches the response for creating it.

    :param get_exercise_response: The API response when requesting exercise data.
    :param create_exercise_response: The API response when creating the exercise.
    :raises AssertionError: If the exercise data does not match.
    """
    assert_exercise(get_exercise_response.exercise, create_exercise_response.exercise)

@allure.step("Check update exercise response")
def assert_update_exercise_response(
    request: UpdateExerciseRequestSchema,
    response: UpdateExerciseResponseSchema,
):
    """
    Checks that the exercise update response corresponds to the data from the request.

    :param request: The original request to update the exercise.
    :param response: The API response with the updated exercise data.
    :raises AssertionError: If at least one field does not match.
    """
    assert_equal(actual=response.exercise.title, expected=request.title, name="title")
    assert_equal(actual=response.exercise.max_score, expected=request.max_score, name="max_score")
    assert_equal(actual=response.exercise.min_score, expected=request.min_score, name="min_score")
    assert_equal(actual=response.exercise.order_index, expected=request.order_index, name="order_index")
    assert_equal(actual=response.exercise.description, expected=request.description, name="description")
    assert_equal(actual=response.exercise.estimated_time, expected=request.estimated_time, name="estimated_time")

@allure.step("Check exercise not found response")
def assert_exercise_not_found_response(actual: InternalErrorResponseSchema):
    """
    Checks that the response for an exercise not found error matches the expected internal error.

    :param actual: The API response with the internal error to check.
    :raises AssertionError: If the actual response does not match the expected "Exercise not found" error.
    """
    expected = InternalErrorResponseSchema(details="Exercise not found")
    assert_internal_error_response(actual, expected)

@allure.step("Check get exercises response")
def assert_get_exercises_response(
    get_exercises_response: GetExercisesResponseSchema,
    create_exercise_responses: list[CreateExerciseResponseSchema],
):
    """
    Checks that the response for getting exercises contains all exercises created previously.

    :param get_exercises_response: The API response when requesting the list of exercises.
    :param create_exercise_responses: The list of API responses from creating exercises.
    :raises AssertionError: If exercise count or data doesn't match.
    """
    assert_length(get_exercises_response.exercises, create_exercise_responses, "exercises")
    for index, create_exercise_response in enumerate(create_exercise_responses):
        assert_exercise(get_exercises_response.exercises[index], create_exercise_response.exercise)
