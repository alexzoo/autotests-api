from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
    ExerciseSchema,
    GetExerciseResponseSchema,
)
from tools.assertions.base import assert_equal


def assert_create_exercise_response(
    request: CreateExerciseRequestSchema, response: CreateExerciseResponseSchema
):
    """
    Checks that the exercise creation response corresponds to the data from the request.

    :param request: The original request to create the exercise.
    :param response: The API response with the created exercise data.
    :raises AssertionError: If at least one field does not match.
    """
    assert_equal(actual=request.title, expected=response.exercise.title, name="title")
    assert_equal(actual=request.course_id, expected=response.exercise.course_id, name="course_id")
    assert_equal(actual=request.max_score, expected=response.exercise.max_score, name="max_score")
    assert_equal(actual=request.min_score, expected=response.exercise.min_score, name="min_score")
    assert_equal(
        actual=request.order_index, expected=response.exercise.order_index, name="order_index"
    )
    assert_equal(
        actual=request.description, expected=response.exercise.description, name="description"
    )
    assert_equal(
        actual=request.estimated_time,
        expected=response.exercise.estimated_time,
        name="estimated_time",
    )


def assert_exercise(actual: ExerciseSchema, expected: ExerciseSchema):
    """
    Checks that the actual exercise matches the expected exercise.

    :param actual: The actual ExercisesSchema object to verify.
    :param expected: The expected ExercisesSchema object to compare against.
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
