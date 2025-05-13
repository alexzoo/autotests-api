import pytest
from pydantic import BaseModel

from clients.exercises.exercises_client import ExercisesClient, get_exercises_client
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
)
from fixtures.courses import CourseFixture
from fixtures.users import UserFixture


class ExercisesFixture(BaseModel):
    request: CreateExerciseRequestSchema
    response: CreateExerciseResponseSchema


@pytest.fixture
def exercise_client(function_user: UserFixture) -> ExercisesClient:
    """
    Creates an ExercisesClient authenticated for the function-scoped user.

    :param function_user: The fixture providing the authenticated user.
    :return: An authenticated ExercisesClient instance.
    """
    return get_exercises_client(function_user.authentication_user)


@pytest.fixture
def function_exercise(
    exercise_client: ExercisesClient, function_course: CourseFixture
) -> ExercisesFixture:
    """
    Creates a test exercise associated with the function-scoped course.

    Generates a new exercise for each test function that requires it and returns
    both the request and response objects.

    :param exercise_client: Client for exercise creation.
    :param function_course: The fixture providing the course to associate the exercise with.
    :return: An ExercisesFixture containing request and response data for the created exercise.
    """
    request = CreateExerciseRequestSchema(course_id=function_course.response.course.id)
    response = exercise_client.create_exercise(request=request)
    return ExercisesFixture(request=request, response=response)
