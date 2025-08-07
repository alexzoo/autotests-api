import allure
from httpx import Request, Response

from tools.http.curl import make_curl_from_request
from tools.logger import get_logger

logger = get_logger("HTTP_CLIENT")


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


def log_request_event_hook(request: Request):
    """
    Logs information about the sent HTTP request.

    Args:
        request: HTTPX request object.
    """
    logger.info(f"Make {request.method} request to {request.url}")


def log_response_event_hook(response: Response):
    """
    Logs information about the received HTTP response.

    Args:
        response: HTTPX response object.
    """
    logger.info(f"Got response {response.status_code} {response.reason_phrase} from {response.url}")
