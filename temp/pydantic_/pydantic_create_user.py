from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    """
    Schema representing user data structure.

    :attr id: Unique identifier of the user.
    :attr email: User's email address.
    :attr last_name: User's last name.
    :attr first_name: User's first name.
    :attr middle_name: User's middle name.
    """
    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")


class CreateUserRequestSchema(BaseModel):
    """
    Schema for user creation request.

    :attr email: User's email address.
    :attr password: User's password.
    :attr last_name: User's last name.
    :attr first_name: User's first name.
    :attr middle_name: User's middle name.
    """
    email: EmailStr
    password: str
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")


class CreateUserResponseSchema(BaseModel):
    """
    Schema for user creation response.

    :attr user: Created user data.
    """
    user: UserSchema
