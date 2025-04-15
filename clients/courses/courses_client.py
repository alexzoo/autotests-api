from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient
from clients.files.files_client import File
from clients.private_http_builder import AuthenticationUserDict, get_private_http_client
from clients.users.private_users_client import User


class Course(TypedDict):
    """
    Description of the course structure.
    """
    id: str
    title: str
    maxScore: int
    minScore: int
    description: str
    previewFile: File
    estimatedTime: str
    createdByUser: User


class GetCoursesQueryDict(TypedDict):
    """
    Description of the request structure for retrieving the list of courses.
    """
    userId: str


class CreateCourseRequestDict(TypedDict):
    """
    Description of the request structure for creating a course.
    """
    title: str
    maxScore: int
    minScore: int
    description: str
    estimatedTime: str
    previewFileId: str
    createdByUserId: str


class CreateCourseResponseDict(TypedDict):
    """
    Description of the response structure for course creation.
    """
    course: Course


class UpdateCourseRequestDict(TypedDict):
    """
    Description of the request structure for updating a course.
    """
    title: str | None
    maxScore: int | None
    minScore: int | None
    description: str | None
    estimatedTime: str | None


class CoursesClient(APIClient):
    """
    Client for working with /api/v1/courses
    """

    def get_courses_api(self, query: GetCoursesQueryDict) -> Response:
        """
        Method to retrieve a list of courses based on query parameters.

        :param query: Dictionary with query parameters for filtering courses.
        :return: The server response as an httpx.Response object.
        """
        return self.get("/api/v1/courses", params=query)

    def get_course_api(self, course_id: str) -> Response:
        """
        Method to retrieve a course by its identifier.

        :param course_id: The identifier of the course.
        :return: The server response as an httpx.Response object.
        """
        return self.get(f"/api/v1/courses/{course_id}")

    def create_course_api(self, request: CreateCourseRequestDict) -> Response:
        """
        Method to create a new course.

        :param request: Dictionary with course data for creation.
        :return: The server response as an httpx.Response object.
        """
        return self.post("/api/v1/courses", json=request)

    def update_course_api(self, course_id: str, request: UpdateCourseRequestDict) -> Response:
        """
        Method to update a course by its identifier.

        :param course_id: The identifier of the course.
        :param request: Dictionary with course data to update.
        :return: The server response as an httpx.Response object.
        """
        return self.patch(f"/api/v1/courses/{course_id}", json=request)

    def delete_course_api(self, course_id: str) -> Response:
        """
        Method to delete a course by its identifier.

        :param course_id: The identifier of the course.
        :return: The server response as an httpx.Response object.
        """
        return self.delete(f"/api/v1/courses/{course_id}")

    def create_course(self, request: CreateCourseRequestDict) -> CreateCourseResponseDict:
        """
        Method to create a new course.

        :param request: Dictionary with course data for creation.
        :return: The JSON response from the API as a CreateCourseResponseDict.
        """
        response = self.create_course_api(request)
        return response.json()


def get_courses_client(user: AuthenticationUserDict) -> CoursesClient:
    """
    Function to create an instance of CoursesClient with a pre-configured HTTP client.

    :param user: User authentication data.
    :return: A ready-to-use CoursesClient.
    """
    return CoursesClient(client=get_private_http_client(user))
