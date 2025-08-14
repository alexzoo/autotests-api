import allure
from httpx import QueryParams, Response

from clients.api_client import APIClient
from clients.api_coverage import tracker
from clients.courses.courses_schema import (
    CreateCourseRequestSchema,
    CreateCourseResponseSchema,
    GetCoursesQuerySchema,
    UpdateCourseRequestSchema,
)
from clients.private_http_builder import AuthenticationUserSchema, get_private_http_client
from tools.routes import APIRoutes


class CoursesClient(APIClient):
    """
    Client for working with /api/v1/courses
    """

    @allure.step("Get courses")
    @tracker.track_coverage_httpx(APIRoutes.COURSES)
    def get_courses_api(self, query: GetCoursesQuerySchema) -> Response:
        """
        Method to retrieve a list of courses based on query parameters.

        :param query: Query parameters for filtering courses as a GetCoursesQuerySchema object.
        :return: The server response as an httpx.Response object.
        """
        return self.get(APIRoutes.COURSES, params=QueryParams(query.model_dump(by_alias=True)))

    @allure.step("Get course by id {course_id}")
    @tracker.track_coverage_httpx(f"{APIRoutes.COURSES}/{{course_id}}")
    def get_course_api(self, course_id: str) -> Response:
        """
        Method to retrieve a course by its identifier.

        :param course_id: The identifier of the course.
        :return: The server response as an httpx.Response object.
        """
        return self.get(f"{APIRoutes.COURSES}/{course_id}")

    @allure.step("Create course")
    @tracker.track_coverage_httpx(APIRoutes.COURSES)
    def create_course_api(self, request: CreateCourseRequestSchema) -> Response:
        """
        Method to create a new course.

        :param request: Course data for creation as a CreateCourseRequestSchema object.
        :return: The server response as an httpx.Response object.
        """
        return self.post(APIRoutes.COURSES, json=request.model_dump(by_alias=True))

    @allure.step("Update course by id {course_id}")
    @tracker.track_coverage_httpx(f"{APIRoutes.COURSES}/{{course_id}}")
    def update_course_api(self, course_id: str, request: UpdateCourseRequestSchema) -> Response:
        """
        Method to update a course by its identifier.

        :param course_id: The identifier of the course.
        :param request: Course data for update as an UpdateCourseRequestSchema object.
        :return: The server response as an httpx.Response object.
        """
        return self.patch(
            f"{APIRoutes.COURSES}/{course_id}", json=request.model_dump(by_alias=True)
        )

    @allure.step("Delete course by id {course_id}")
    @tracker.track_coverage_httpx(f"{APIRoutes.COURSES}/{{course_id}}")
    def delete_course_api(self, course_id: str) -> Response:
        """
        Method to delete a course by its identifier.

        :param course_id: The identifier of the course.
        :return: The server response as an httpx.Response object.
        """
        return self.delete(f"{APIRoutes.COURSES}/{course_id}")

    def create_course(self, request: CreateCourseRequestSchema) -> CreateCourseResponseSchema:
        """
        Method to create a new course.

        :param request: Course data for creation as a CreateCourseRequestSchema object.
        :return: The created course as a CreateCourseResponseSchema object.
        """
        response = self.create_course_api(request)
        return CreateCourseResponseSchema.model_validate_json(response.text)


def get_courses_client(user: AuthenticationUserSchema) -> CoursesClient:
    """
    Function to create an instance of CoursesClient with a pre-configured HTTP client.

    :param user: User authentication data.
    :return: A ready-to-use CoursesClient.
    """
    return CoursesClient(client=get_private_http_client(user))
