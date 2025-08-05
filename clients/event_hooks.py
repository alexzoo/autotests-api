import allure
from httpx import Request

from tools.http.curl import make_curl_from_request


def curl_event_hook(request: Request):
    """
    Event hook for automatically attaching cURL command to Allure report.

    This function generates a cURL command from the HTTP request object and
    attaches it to the Allure test report as a text attachment for debugging
    and documentation purposes.

    Args:
        request (Request): HTTP request object passed to the httpx client.

    Returns:
        None

    Note:
        This function is designed to be used as an event hook with httpx client
        to automatically capture and attach cURL commands to test reports.
    """

    curl_command = make_curl_from_request(request)

    allure.attach(curl_command, "cURL command", allure.attachment_type.TEXT)
