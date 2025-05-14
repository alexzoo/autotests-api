from http import HTTPStatus

import allure
import pytest

from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
    GetExerciseResponseSchema,
    GetExercisesQuerySchema,
    GetExercisesResponseSchema,
    UpdateExerciseRequestSchema,
    UpdateExerciseResponseSchema,
)
from fixtures.courses import CourseFixture
from fixtures.exercises import ExercisesFixture
from tools.allure.tag import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import (
    assert_create_exercise_response,
    assert_exercise_not_found_response,
    assert_get_exercise_response,
    assert_get_exercises_response,
    assert_update_exercise_response,
)
from tools.assertions.schema import validate_json_schema


@pytest.mark.exercises
@pytest.mark.regression
class TestExercises:
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.title("Create exercise")
    def test_create_exercise(
        self,
        exercise_client: ExercisesClient,
        function_course: CourseFixture,
    ):
        request = CreateExerciseRequestSchema(course_id=function_course.response.course.id)
        response = exercise_client.create_exercise_api(request)
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_exercise_response(request, response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.title("Get exercise")
    def test_get_exercise(
        self,
        exercise_client: ExercisesClient,
        function_exercise: ExercisesFixture,
    ):
        response = exercise_client.get_exercise_api(
            exercise_id=function_exercise.response.exercise.id
        )
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_exercise_response(
            response_data,
            function_exercise.response,
        )
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.title("Update exercise")
    def test_update_exercise(
        self,
        exercise_client: ExercisesClient,
        function_exercise: ExercisesFixture,
    ):
        request = UpdateExerciseRequestSchema()
        response = exercise_client.update_exercise_api(
            function_exercise.response.exercise.id,
            request,
        )
        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_exercise_response(request, response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.DELETE_ENTITY)
    @allure.title("Delete exercise")
    def test_delete_exercise(
        self,
        exercise_client: ExercisesClient,
        function_exercise: ExercisesFixture,
    ):
        delete_response = exercise_client.delete_exercise_api(
            function_exercise.response.exercise.id
        )
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        get_response = exercise_client.get_exercise_api(function_exercise.response.exercise.id)
        get_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)

        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
        assert_exercise_not_found_response(get_response_data)

        validate_json_schema(get_response.json(), get_response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.title("Get exercises")
    def test_get_exercises(
        self,
        exercise_client: ExercisesClient,
        function_exercise: ExercisesFixture,
        function_course: CourseFixture,
    ):
        query = GetExercisesQuerySchema(course_id=function_course.response.course.id)
        response = exercise_client.get_exercises_api(query)
        response_data = GetExercisesResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_exercises_response(
            response_data,
            [function_exercise.response],
        )
        validate_json_schema(response.json(), response_data.model_json_schema())
