from typing import TypedDict

from httpx import Client

from clients.authentication.authentication_client import get_authentication_client, LoginRequestDict


class AuthenticationUserDict(TypedDict):
    email: str
    password: str


def get_private_http_client(user: AuthenticationUserDict) -> Client:
    """
    Function creates an instance of httpx.Client with user authentication.

    :param user: AuthenticationUserDict object with user's email and password.
    :return: Ready-to-use httpx.Client object with Authorization header set.
    """
    authentication_client = get_authentication_client()
    login_request = LoginRequestDict(email=user['email'], password=user['password'])
    login_response = authentication_client.login(login_request)

    return Client(
        timeout=100,
        base_url="http://localhost:8000",
        headers={"Authorization": f"Bearer {login_response['token']['accessToken']}"}
    )
