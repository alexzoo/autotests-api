from httpx import Response

from clients.api_client import APIClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, \
    CreateExerciseResponseSchema, GetExerciseResponseSchema, GetExercisesQuerySchema, \
    GetExercisesResponseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema
from clients.private_http_builder import AuthenticationUserSchema, get_private_http_client


class ExercisesClient(APIClient):
    """
    Client for exercises API operations.
    """

    def get_exercises_api(self, query: GetExercisesQuerySchema) -> Response:
        """
        Method to retrieve a list of exercises based on query parameters.

        :param query: Dictionary with query parameters for filtering exercises.
        :return: The server response as an httpx.Response object.
        """
        return self.get("/api/v1/exercises", params=query.model_dump(by_alias=True))

    def get_exercise_api(self, exercise_id: str) -> Response:
        """
        Method to retrieve a specific exercise by ID.

        :param exercise_id: The identifier of the exercise.
        :return: The server response as an httpx.Response object.
        """
        return self.get(f"/api/v1/exercises/{exercise_id}")

    def create_exercise_api(self, request: CreateExerciseRequestSchema) -> Response:
        """
        Method to create a new exercise.

        :param request: Dictionary with exercise data for creation.
        :return: The server response as an httpx.Response object.
        """
        return self.post("/api/v1/exercises", json=request.model_dump(by_alias=True))

    def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequestSchema) -> Response:
        """
        Method to update an existing exercise.

        :param exercise_id: The identifier of the exercise to update.
        :param request: Dictionary with exercise data to update.
        :return: The server response as an httpx.Response object.
        """
        return self.patch(f"/api/v1/exercises/{exercise_id}",
                          json=request.model_dump(by_alias=True))

    def delete_exercise_api(self, exercise_id: str) -> Response:
        """
        Method to delete an exercise.

        :param exercise_id: The identifier of the exercise to delete.
        :return: The server response as an httpx.Response object.
        """
        return self.delete(f"/api/v1/exercises/{exercise_id}")

    def get_exercises(self, query: GetExercisesQuerySchema) -> GetExercisesResponseSchema:
        """
        Method to retrieve a list of exercises based on query parameters.

        :param query: Dictionary with query parameters for filtering exercises.
        :return: Parsed JSON response containing exercises data.
        """
        response = self.get_exercises_api(query)
        return GetExercisesResponseSchema.model_validate_json(response.text)

    def get_exercise(self, exercise_id: str) -> GetExerciseResponseSchema:
        """
        Method to retrieve a specific exercise by ID.

        :param exercise_id: The identifier of the exercise.
        :return: Parsed JSON response containing exercise data.
        """
        response = self.get_exercise_api(exercise_id)
        return GetExerciseResponseSchema.model_validate_json(response.text)

    def create_exercise(self, request: CreateExerciseRequestSchema) -> CreateExerciseResponseSchema:
        """
        Method to create a new exercise.

        :param request: Dictionary with exercise data for creation.
        :return: Parsed JSON response containing the created exercise data.
        """
        response = self.create_exercise_api(request)
        return CreateExerciseResponseSchema.model_validate_json(response.text)

    def update_exercise(
        self,
        exercise_id: str,
        request: UpdateExerciseRequestSchema
    ) -> UpdateExerciseResponseSchema:
        """
        Method to update an existing exercise.

        :param exercise_id: The identifier of the exercise to update.
        :param request: Dictionary with exercise data to update.
        :return: Parsed JSON response containing the updated exercise data.
        """
        response = self.update_exercise_api(
            exercise_id,
            request)
        return UpdateExerciseResponseSchema.model_validate_json(response.text)


def get_exercises_client(user: AuthenticationUserSchema) -> ExercisesClient:
    """
    Function that creates an instance of ExercisesClient with a preconfigured HTTP client.

    :param user: User authentication details.
    :return: A ready-to-use ExercisesClient.
    """
    return ExercisesClient(get_private_http_client(user))
