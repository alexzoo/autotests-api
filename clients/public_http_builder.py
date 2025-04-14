from httpx import Client


def get_public_http_client() -> Client:
    """
    Function creates an instance of httpx.Client with basic settings.

    :return: Ready-to-use httpx.Client object.
    """
    return Client(timeout=100, base_url="http://localhost:8000")
