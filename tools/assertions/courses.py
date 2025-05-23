from clients.courses.courses_schema import (
    CourseSchema,
    CreateCourseRequestSchema,
    CreateCourseResponseSchema,
    GetCoursesResponseSchema,
    UpdateCourseRequestSchema,
    UpdateCourseResponseSchema,
)
from tools.assertions.base import assert_equal, assert_length
from tools.assertions.files import assert_file
from tools.assertions.users import assert_user


def assert_update_course_response(
    request: UpdateCourseRequestSchema,
    response: UpdateCourseResponseSchema,
):
    """
    Checks that the course update response corresponds to the data from the request.

    :param request: The original request to update the course.
    :param response: The API response with the updated course data.
    :raises AssertionError: If at least one field does not match.
    """
    assert_equal(response.course.title, request.title, "title")
    assert_equal(response.course.max_score, request.max_score, "max_score")
    assert_equal(response.course.min_score, request.min_score, "min_score")
    assert_equal(response.course.description, request.description, "description")
    assert_equal(response.course.estimated_time, request.estimated_time, "estimated_time")


def assert_course(actual: CourseSchema, expected: CourseSchema):
    """
    Checks that the actual course data matches the expected data.

    :param actual: The actual course data.
    :param expected: The expected course data.
    :raises AssertionError: If at least one field does not match.
    """
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")

    assert_file(actual.preview_file, expected.preview_file)
    assert_user(actual.created_by_user, expected.created_by_user)


def assert_get_courses_response(
    get_courses_response: GetCoursesResponseSchema,
    create_course_responses: list[CreateCourseResponseSchema],
):
    """
    Checks that the response for getting the list of courses matches the responses from creating them.

    :param get_courses_response: The API response when requesting the list of courses.
    :param create_course_responses: The list of API responses from creating the courses.
    :raises AssertionError: If the course data does not match.
    """
    assert_length(get_courses_response.courses, create_course_responses, "courses")

    for index, create_course_response in enumerate(create_course_responses):
        assert_course(get_courses_response.courses[index], create_course_response.course)


def assert_create_course_response(
    request: CreateCourseRequestSchema,
    response: CreateCourseResponseSchema,
):
    """
    Checks that the course creation response corresponds to the data from the request.

    :param request: The original request to create the course.
    :param response: The API response with the created course data.
    :raises AssertionError: If at least one field does not match.
    """
    assert_equal(actual=request.title, expected=response.course.title, name="title")
    assert_equal(actual=request.max_score, expected=response.course.max_score, name="max_score")
    assert_equal(actual=request.min_score, expected=response.course.min_score, name="min_score")
    assert_equal(
        actual=request.description, expected=response.course.description, name="description"
    )
    assert_equal(
        actual=request.estimated_time,
        expected=response.course.estimated_time,
        name="estimated_time",
    )
    assert_equal(
        actual=request.preview_file_id,
        expected=response.course.preview_file.id,
        name="preview_file_id",
    )
    assert_equal(
        actual=request.created_by_user_id,
        expected=response.course.created_by_user.id,
        name="created_by_user_id",
    )
