from pydantic import BaseModel, Field

from tools.fakers import fake


class TokenSchema(BaseModel):
    """
    Description of the authentication tokens structure.
    """

    token_type: str = Field(alias=str("tokenType"))
    access_token: str = Field(alias=str("accessToken"))
    refresh_token: str = Field(alias=str("refreshToken"))


class LoginRequestSchema(BaseModel):
    """
    Description of the authentication request structure.
    """

    email: str = Field(default_factory=fake.email)
    password: str = Field(default_factory=fake.password)


class LoginResponseSchema(BaseModel):
    """
    Description of the authentication response structure.
    """

    token: TokenSchema


class RefreshRequestSchema(BaseModel):
    """
    Description of the request structure for token refresh.
    """

    refresh_token: str = Field(alias=str("refreshToken"), default_factory=fake.sentence)
