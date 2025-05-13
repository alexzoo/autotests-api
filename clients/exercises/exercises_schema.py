from pydantic import BaseModel, ConfigDict, Field

from tools.fakers import fake


class ExerciseSchema(BaseModel):
    """
    Structure of an exercise entity.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    course_id: str = Field(alias=str("courseId"))
    max_score: int = Field(alias=str("maxScore"))
    min_score: int = Field(alias=str("minScore"))
    order_index: int = Field(alias=str("orderIndex"))
    description: str
    estimated_time: str = Field(alias=str("estimatedTime"))


class GetExercisesQuerySchema(BaseModel):
    """
    Description of the query parameters for retrieving exercises.
    """

    model_config = ConfigDict(populate_by_name=True)

    course_id: str = Field(alias=str("courseId"))


class GetExercisesResponseSchema(BaseModel):
    """
    Structure of the response when retrieving a list of exercises.
    """

    exercises: list[ExerciseSchema]


class GetExerciseResponseSchema(BaseModel):
    """
    Structure of the response when retrieving a single exercise.
    """

    exercise: ExerciseSchema


class CreateExerciseRequestSchema(BaseModel):
    """
    Description of the request structure for creating an exercise.
    """

    model_config = ConfigDict(populate_by_name=True)

    title: str = Field(default_factory=fake.sentence)
    course_id: str = Field(alias=str("courseId"), default_factory=fake.uuid4)
    max_score: int = Field(alias=str("maxScore"), default_factory=fake.max_score)
    min_score: int = Field(alias=str("minScore"), default_factory=fake.min_score)
    order_index: int = Field(alias=str("orderIndex"), default_factory=fake.integer)
    description: str = Field(default_factory=fake.text)
    estimated_time: str = Field(alias=str("estimatedTime"), default_factory=fake.estimated_time)


class CreateExerciseResponseSchema(BaseModel):
    """
    Structure of the response when creating an exercise.
    """

    exercise: ExerciseSchema


class UpdateExerciseRequestSchema(BaseModel):
    """
    Description of the request structure for updating an exercise.
    """

    model_config = ConfigDict(populate_by_name=True)

    title: str | None = Field(default_factory=fake.sentence)
    max_score: int | None = Field(alias=str("maxScore"), default_factory=fake.max_score)
    min_score: int | None = Field(alias=str("minScore"), default_factory=fake.min_score)
    order_index: int | None = Field(alias=str("orderIndex"), default_factory=fake.integer)
    description: str | None = Field(default_factory=fake.text)
    estimated_time: str | None = Field(
        alias=str("estimatedTime"), default_factory=fake.estimated_time
    )


class UpdateExerciseResponseSchema(BaseModel):
    """
    Structure of the response when updating an exercise.
    """

    exercise: ExerciseSchema
