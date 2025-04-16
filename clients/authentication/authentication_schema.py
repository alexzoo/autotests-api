from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    """
    Description of the authentication tokens structure.
    """
    token_type: str = Field(alias="tokenType")
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")


class LoginRequestSchema(BaseModel):
    """
    Description of the authentication request structure.
    """
    email: str
    password: str


class LoginResponseSchema(BaseModel):
    """
    Description of the authentication response structure.
    """
    token: TokenSchema


class RefreshRequestSchema(BaseModel):
    """
    Description of the request structure for token refresh.
    """
    refresh_token: str = Field(alias="refreshToken")
