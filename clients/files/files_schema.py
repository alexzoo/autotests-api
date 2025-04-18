from pydantic import BaseModel, Field, HttpUrl
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
    filename: str = Field(default_factory=lambda: f'{fake.uuid4()}.png')
    directory: str = Field(default="tests")
    upload_file: str


class CreateFileResponseSchema(BaseModel):
    """
    Description of the response structure for creating a file.
    """
    file: FileSchema
