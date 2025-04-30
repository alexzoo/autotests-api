from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ValidationErrorSchema(BaseModel):
    """
    Model describing the structure of an API validation error.
    """

    model_config = ConfigDict(populate_by_name=True)

    type: str
    input: Any
    context: dict[str, Any] = Field(alias=str("ctx"))
    message: str = Field(alias=str("msg"))
    location: list[str] = Field(alias=str("loc"))


class ValidationErrorResponseSchema(BaseModel):
    """
    Model describing the structure of an API response with a validation error.
    """

    model_config = ConfigDict(populate_by_name=True)

    details: list[ValidationErrorSchema] = Field(alias=str("detail"))


class InternalErrorResponseSchema(BaseModel):
    """
    Model describing an internal error.
    """

    model_config = ConfigDict(populate_by_name=True)

    details: str = Field(alias=str("detail"))
