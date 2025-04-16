from pydantic import BaseModel, HttpUrl


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
    filename: str
    directory: str
    upload_file: str


class CreateFileResponseSchema(BaseModel):
    """
    Description of the response structure for creating a file.
    """
    file: FileSchema
