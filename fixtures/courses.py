import pytest
from pydantic import BaseModel

from clients.courses.courses_client import CoursesClient, get_courses_client
from clients.courses.courses_schema import CreateCourseRequestSchema, CreateCourseResponseSchema
from fixtures.files import FileFixture
from fixtures.users import UserFixture


class CourseFixture(BaseModel):
    request: CreateCourseRequestSchema
    response: CreateCourseResponseSchema


@pytest.fixture
def course_client(function_user: UserFixture) -> CoursesClient:
    """
    Creates a course client authenticated as the function-scoped user.
    :param function_user: The user fixture for the current test function.
    :return: An authenticated CoursesClient instance.
    """
    return get_courses_client(function_user.authentication_user)


@pytest.fixture
def function_course(
    course_client: CoursesClient, function_user: UserFixture, function_file: FileFixture
) -> CourseFixture:
    """
    Creates a test course for the current test function.
    Generates a new course using the function-scoped user and file,
    and returns both the request and response objects.
    :param course_client: Client for course creation.
    :param function_user: The user fixture for the current test function.
    :param function_file: The file fixture for the current test function.
    :return: A CourseFixture containing request and response data.
    """
    request = CreateCourseRequestSchema(
        previewFileId=function_file.response.file.id,
        createdByUserId=function_user.response.user.id,
    )
    response = course_client.create_course(request=request)
    return CourseFixture(request=request, response=response)
