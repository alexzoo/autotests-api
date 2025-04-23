import pytest
from pydantic import BaseModel, EmailStr

from clients.authentication.authentication_client import (
    AuthenticationClient,
    get_authentication_client,
)
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.private_users_client import PrivateUsersClient, get_private_users_client
from clients.users.public_users_client import PublicUsersClient, get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema


class UserFixture(BaseModel):
    request: CreateUserRequestSchema
    response: CreateUserResponseSchema

    @property
    def email(self) -> EmailStr:
        return self.request.email

    @property
    def password(self) -> str:
        return self.request.password

    @property
    def authentication_user(self) -> AuthenticationUserSchema:
        return AuthenticationUserSchema(email=self.email, password=self.password)


@pytest.fixture
def authentication_client() -> AuthenticationClient:
    """
    Provides an instance of the authentication client.
    Creates and returns a new authentication client for API tests.
    :return: An instance of AuthenticationClient
    """
    return get_authentication_client()


@pytest.fixture
def public_users_client() -> PublicUsersClient:
    """
    Provides an instance of the public users client.
    Creates and returns a new public users client for API tests.
    :return: An instance of PublicUsersClient
    """
    return get_public_users_client()


@pytest.fixture
def function_user(public_users_client: PublicUsersClient) -> UserFixture:
    """
    Creates a test user for the current test function.
    Generates a new user for each test function that requires it and returns
    both the request and response objects.
    :param public_users_client: Client for user creation
    :return: A UserFixture containing request and response data
    """
    request = CreateUserRequestSchema()
    response = public_users_client.create_user(request)
    return UserFixture(request=request, response=response)


@pytest.fixture
def private_users_client(function_user: UserFixture) -> PrivateUsersClient:
    """
    Provides an authenticated private users client.
    Creates a client using the credentials from the function_user fixture.
    :param function_user: User fixture with authentication credentials
    :return: An authenticated instance of PrivateUsersClient
    """
    return get_private_users_client(function_user.authentication_user)
