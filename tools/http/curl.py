from httpx import Request, RequestNotRead


def make_curl_from_request(request: Request) -> str:
    """
    Generates a cURL command from an httpx HTTP request.

    :param request: HTTP request from which the cURL command will be formed.
    :return: String with cURL command containing request method, URL, headers and body (if present).
    """
    result: list[str] = [f"curl -X '{request.method}'", f"'{request.url}'"]

    for header, value in request.headers.items():
        result.append(f"-H '{header}: {value}'")

    try:
        if body := request.content:
            result.append(f"-d '{body.decode('utf-8')}'")
    except RequestNotRead:
        pass

    return " \\\n  ".join(result)
