from pydantic import BaseModel, ConfigDict, Field


class Exercise(BaseModel):
    """
    Structure of an exercise entity.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    course_id: str = Field(alias="courseId")
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    order_index: int = Field(alias="orderIndex")
    description: str
    estimated_time: str = Field(alias="estimatedTime")


class GetExercisesQuerySchema(BaseModel):
    """
    Description of the query parameters for retrieving exercises.
    """
    model_config = ConfigDict(populate_by_name=True)

    course_id: str = Field(alias="courseId")


class GetExercisesResponseSchema(BaseModel):
    """
    Structure of the response when retrieving a list of exercises.
    """
    exercises: list[Exercise]


class GetExerciseResponseSchema(BaseModel):
    """
    Structure of the response when retrieving a single exercise.
    """
    exercise: Exercise


class CreateExerciseRequestSchema(BaseModel):
    """
    Description of the request structure for creating an exercise.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str
    course_id: str = Field(alias="courseId")
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    order_index: int = Field(alias="orderIndex")
    description: str
    estimated_time: str = Field(alias="estimatedTime")


class CreateExerciseResponseSchema(BaseModel):
    """
    Structure of the response when creating an exercise.
    """
    exercise: Exercise


class UpdateExerciseRequestSchema(BaseModel):
    """
    Description of the request structure for updating an exercise.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str | None
    max_score: int | None = Field(alias="maxScore")
    min_score: int | None = Field(alias="minScore")
    order_index: int | None = Field(alias="orderIndex")
    description: str | None
    estimated_time: str | None = Field(alias="estimatedTime")


class UpdateExerciseResponseSchema(BaseModel):
    """
    Structure of the response when updating an exercise.
    """
    exercise: Exercise
