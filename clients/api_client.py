from typing import Any

import allure
from httpx import URL, Client, QueryParams, Response
from httpx._types import RequestData, RequestFiles


class APIClient:
    def __init__(self, client: Client):
        """
        Base API client that accepts an httpx.Client object.

        :param client: an instance of httpx.Client for making HTTP requests
        """
        self.client = client

    @allure.step("Make GET request to {url}")
    def get(self, url: URL | str, params: QueryParams | None = None) -> Response:
        """
        Performs a GET request.

        :param url: Endpoint URL.
        :param params: GET request parameters (e.g., ?key=value).
        :return: Response object with response data.
        """
        return self.client.get(url, params=params)

    @allure.step("Make POST request to {url}")
    def post(
        self,
        url: URL | str,
        json: Any | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
    ) -> Response:
        """
        Performs a POST request.

        :param url: Endpoint URL.
        :param json: Data in JSON format.
        :param data: Formatted form data (e.g., application/x-www-form-urlencoded).
        :param files: Files to upload to the server.
        :return: Response object with response data.
        """
        return self.client.post(url, json=json, data=data, files=files)

    @allure.step("Make PATCH request to {url}")
    def patch(self, url: URL | str, json: Any | None = None) -> Response:
        """
        Performs a PATCH request (partial data update).

        :param url: Endpoint URL.
        :param json: Data to update in JSON format.
        :return: Response object with response data.
        """
        return self.client.patch(url, json=json)

    @allure.step("Make DELETE request to {url}")
    def delete(self, url: URL | str) -> Response:
        """
        Performs a DELETE request (data deletion).

        :param url: Endpoint URL.
        :return: Response object with response data.
        """
        return self.client.delete(url)
