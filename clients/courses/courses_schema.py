from pydantic import BaseModel, ConfigDict, Field

from clients.files.files_schema import FileSchema
from clients.users.users_schema import UserSchema
from tools.fakers import fake


class CourseSchema(BaseModel):
    """
    Description of the course structure.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    max_score: int = Field(alias=str("maxScore"))
    min_score: int = Field(alias=str("minScore"))
    description: str
    preview_file: FileSchema = Field(alias=str("previewFile"))
    estimated_time: str = Field(alias=str("estimatedTime"))
    created_by_user: UserSchema = Field(alias=str("createdByUser"))


class GetCoursesQuerySchema(BaseModel):
    """
    Description of the request structure for retrieving the list of courses.
    """

    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias=str("userId"))


class GetCoursesResponseSchema(BaseModel):
    """
    Description of the response structure for retrieving the list of courses.
    """

    courses: list[CourseSchema]


class CreateCourseRequestSchema(BaseModel):
    """
    Description of the request structure for creating a course.
    """

    model_config = ConfigDict(populate_by_name=True)

    title: str = Field(default_factory=fake.sentence)
    max_score: int = Field(alias=str("maxScore"), default_factory=fake.max_score)
    min_score: int = Field(alias=str("minScore"), default_factory=fake.min_score)
    description: str = Field(default_factory=fake.text)
    estimated_time: str = Field(alias=str("estimatedTime"), default_factory=fake.estimated_time)
    preview_file_id: str = Field(alias=str("previewFileId"), default_factory=fake.uuid4)
    created_by_user_id: str = Field(alias=str("createdByUserId"), default_factory=fake.uuid4)


class CreateCourseResponseSchema(BaseModel):
    """
    Description of the response structure for course creation.
    """

    course: CourseSchema


class UpdateCourseRequestSchema(BaseModel):
    """
    Description of the request structure for updating a course.
    """

    model_config = ConfigDict(populate_by_name=True)

    title: str | None = Field(default_factory=fake.sentence)
    max_score: int | None = Field(alias=str("maxScore"), default_factory=fake.max_score)
    min_score: int | None = Field(alias=str("minScore"), default_factory=fake.min_score)
    description: str | None = Field(default_factory=fake.text)
    estimated_time: str | None = Field(
        alias=str("estimatedTime"), default_factory=fake.estimated_time
    )


class UpdateCourseResponseSchema(BaseModel):
    """
    Description of the response structure for updating a course.
    """

    course: CourseSchema
