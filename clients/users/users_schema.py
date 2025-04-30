from pydantic import BaseModel, ConfigDict, EmailStr, Field

from tools.fakers import fake


class UserSchema(BaseModel):
    """
    User structure description.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str
    email: EmailStr
    last_name: str = Field(alias=str("lastName"))
    first_name: str = Field(alias=str("firstName"))
    middle_name: str = Field(alias=str("middleName"))


class CreateUserRequestSchema(BaseModel):
    """
    Description of the user creation request structure.
    """

    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr = Field(default_factory=fake.email)
    password: str = Field(default_factory=fake.password)
    last_name: str = Field(alias=str("lastName"), default_factory=fake.last_name)
    first_name: str = Field(alias=str("firstName"), default_factory=fake.first_name)
    middle_name: str = Field(alias=str("middleName"), default_factory=fake.middle_name)


class CreateUserResponseSchema(BaseModel):
    """
    Description of the user creation response structure.
    """

    user: UserSchema


class UpdateUserRequestSchema(BaseModel):
    """
    Description of the structure of the request to update a user.
    """

    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr | None = Field(default_factory=fake.email)
    last_name: str | None = Field(alias=str("lastName"), default_factory=fake.last_name)
    first_name: str | None = Field(alias=str("firstName"), default_factory=fake.first_name)
    middle_name: str | None = Field(alias=str("middleName"), default_factory=fake.middle_name)


class UpdateUserResponseSchema(BaseModel):
    """
    Description of the structure of the response to update a user.
    """

    user: UserSchema


class GetUserResponseSchema(BaseModel):
    """
    Description of the structure of the response to get a user.
    """

    user: UserSchema
