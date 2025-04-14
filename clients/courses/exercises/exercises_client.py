from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient
from clients.private_http_builder import AuthenticationUserDict, get_private_http_client


class Exercise(TypedDict):
    id: str
    title: str
    courseId: str
    maxScore: int
    minScore: int
    orderIndex: int
    description: str
    estimatedTime: str


class GetExercisesQueryDict(TypedDict):
    """
    Description of the query parameters for retrieving exercises.
    """
    courseId: str


class GetExercisesResponseDict(TypedDict):
    exercises: list[Exercise]


class GetExerciseResponseDict(TypedDict):
    exercise: Exercise


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


class CreateExerciseResponseDict(TypedDict):
    exercise: Exercise


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


class UpdateExerciseResponseDict(TypedDict):
    exercise: Exercise


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

    def get_exercises(self, query: GetExercisesQueryDict) -> GetExercisesResponseDict:
        """
        Method to retrieve a list of exercises based on query parameters.

        :param query: Dictionary with query parameters for filtering exercises.
        :return: Parsed JSON response containing exercises data.
        """
        response = self.get_exercises_api(query)
        return response.json()

    def get_exercise(self, exercise_id: str) -> GetExerciseResponseDict:
        """
        Method to retrieve a specific exercise by ID.

        :param exercise_id: The identifier of the exercise.
        :return: Parsed JSON response containing exercise data.
        """
        response = self.get_exercise_api(exercise_id)
        return response.json()

    def create_exercise(self, request: CreateExerciseRequestDict) -> CreateExerciseResponseDict:
        """
        Method to create a new exercise.

        :param request: Dictionary with exercise data for creation.
        :return: Parsed JSON response containing the created exercise data.
        """
        response = self.create_exercise_api(request)
        return response.json()

    def update_exercise(self,
                        exercise_id: str,
                        request: UpdateExerciseRequestDict
                        ) -> UpdateExerciseResponseDict:
        """
        Method to update an existing exercise.

        :param exercise_id: The identifier of the exercise to update.
        :param request: Dictionary with exercise data to update.
        :return: Parsed JSON response containing the updated exercise data.
        """
        response = self.update_exercise_api(exercise_id, request)
        return response.json()


def get_exercises_client(user: AuthenticationUserDict) -> ExercisesClient:
    """
    Function that creates an instance of ExercisesClient with a preconfigured HTTP client.

    :param user: User authentication details.
    :return: A ready-to-use ExercisesClient.
    """
    return ExercisesClient(get_private_http_client(user))
