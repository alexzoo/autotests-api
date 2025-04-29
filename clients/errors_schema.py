from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ValidationErrorSchema(BaseModel):
    """
    Model describing the structure of an API validation error.
    """

    model_config = ConfigDict(populate_by_name=True)

    type: str
    input: Any
    context: dict[str, Any] = Field(alias="ctx")
    message: str = Field(alias="msg")
    location: list[str] = Field(alias="loc")


class ValidationErrorResponseSchema(BaseModel):
    """
    Model describing the structure of an API response with a validation error.
    """

    model_config = ConfigDict(populate_by_name=True)

    details: list[ValidationErrorSchema] = Field(alias="detail")


class InternalErrorResponseSchema(BaseModel):
    """
    Model describing an internal error.
    """

    model_config = ConfigDict(populate_by_name=True)

    details: str = Field(alias="detail")
