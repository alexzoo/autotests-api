from pydantic import BaseModel, Field, HttpUrl
import pydantic

from tools.fakers import fake


class FileSchema(BaseModel):
    """
    Description of the file structure.
    """

    id: str
    url: HttpUrl
    filename: str
    directory: str


class CreateFileRequestSchema(BaseModel):
    """
    Description of the request structure for creating a file.
    """

    filename: str = Field(default_factory=lambda: f"{fake.uuid4()}.png")
    directory: str = Field(default="tests")
    upload_file: pydantic.FilePath


class CreateFileResponseSchema(BaseModel):
    """
    Description of the response structure for creating a file.
    """

    file: FileSchema


class GetFileResponseSchema(BaseModel):
    """
    Description of the response structure for getting a file.
    """

    file: FileSchema
