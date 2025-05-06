

from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from tools.assertions.base import assert_equal


def assert_create_exercise_response(request: CreateExerciseRequestSchema, response: CreateExerciseResponseSchema):
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
    assert_equal(actual=request.order_index, expected=response.exercise.order_index, name="order_index")
    assert_equal(actual=request.description, expected=response.exercise.description, name="description")
    assert_equal(actual=request.estimated_time, expected=response.exercise.estimated_time, name="estimated_time")
