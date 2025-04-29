from http import HTTPStatus

import pytest

from clients.courses.courses_client import CoursesClient
from clients.courses.courses_schema import (
    CreateCourseRequestSchema,
    CreateCourseResponseSchema,
    GetCoursesQuerySchema,
    GetCoursesResponseSchema,
    UpdateCourseRequestSchema,
    UpdateCourseResponseSchema,
)
from fixtures.courses import CourseFixture
from fixtures.files import FileFixture
from fixtures.users import UserFixture
from tools.assertions.base import assert_status_code
from tools.assertions.courses import (
    assert_create_course_response,
    assert_get_courses_response,
    assert_update_course_response,
)
from tools.assertions.schema import validate_json_schema


@pytest.mark.courses
@pytest.mark.regression
class TestCourses:
    def test_create_course(
        self,
        course_client: CoursesClient,
        function_file: FileFixture,
        function_user: UserFixture,
    ):
        request = CreateCourseRequestSchema(
            previewFileId=function_file.response.file.id,
            createdByUserId=function_user.response.user.id,
        )
        response = course_client.create_course_api(request)
        response_data = CreateCourseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_course_response(request=request, response=response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_courses(
        self,
        course_client: CoursesClient,
        function_user: UserFixture,
        function_course: CourseFixture,
    ):
        query = GetCoursesQuerySchema(userId=function_user.response.user.id)
        response = course_client.get_courses_api(query)
        response_data = GetCoursesResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_courses_response(
            get_courses_response=response_data,
            create_course_responses=[function_course.response],
        )
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_update_course(self, course_client: CoursesClient, function_course: CourseFixture):
        request = UpdateCourseRequestSchema()
        response = course_client.update_course_api(
            function_course.response.course.id,
            request,
        )
        response_data = UpdateCourseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_course_response(request=request, response=response_data)
        validate_json_schema(response.json(), response_data.model_json_schema())
