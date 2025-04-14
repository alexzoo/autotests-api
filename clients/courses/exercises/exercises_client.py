from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient


class GetExercisesQueryDict(TypedDict):
    """
    Description of the query parameters for retrieving exercises.
    """
    courseId: str


class CreateExerciseRequestDict(TypedDict):
    """
    Description of the request structure for creating an exercise.
    """
    title: str
    courseId: str
    maxScore: int
    minScore: int
    orderIndex: int
    description: str
    estimatedTime: str


class UpdateExerciseRequestDict(TypedDict):
    """
    Description of the request structure for updating an exercise.
    """
    title: str | None
    maxScore: int | None
    minScore: int | None
    orderIndex: int | None
    description: str | None
    estimatedTime: str | None


class ExercisesClient(APIClient):
    """
    Client for exercises API operations.
    """

    def get_exercises_api(self, query: GetExercisesQueryDict) -> Response:
        """
        Method to retrieve a list of exercises based on query parameters.

        :param query: Dictionary with query parameters for filtering exercises.
        :return: The server response as an httpx.Response object.
        """
        return self.get("/api/v1/exercises", params=query)

    def get_exercise_api(self, exercise_id: str) -> Response:
        """
        Method to retrieve a specific exercise by ID.

        :param exercise_id: The identifier of the exercise.
        :return: The server response as an httpx.Response object.
        """
        return self.get(f"/api/v1/exercises/{exercise_id}")

    def create_exercise_api(self, request: CreateExerciseRequestDict) -> Response:
        """
        Method to create a new exercise.

        :param request: Dictionary with exercise data for creation.
        :return: The server response as an httpx.Response object.
        """
        return self.post("/api/v1/exercises", json=request)

    def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequestDict) -> Response:
        """
        Method to update an existing exercise.

        :param exercise_id: The identifier of the exercise to update.
        :param request: Dictionary with exercise data to update.
        :return: The server response as an httpx.Response object.
        """
        return self.patch(f"/api/v1/exercises/{exercise_id}", json=request)

    def delete_exercise_api(self, exercise_id: str) -> Response:
        """
        Method to delete an exercise.

        :param exercise_id: The identifier of the exercise to delete.
        :return: The server response as an httpx.Response object.
        """
        return self.delete(f"/api/v1/exercises/{exercise_id}")
