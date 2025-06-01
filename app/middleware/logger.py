import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class LoggerMiddleware(BaseHTTPMiddleware):
    """Middleware to log request and response details.

    This middleware logs important information about incoming requests and outgoing
    responses, such as request URL, method, size, response status, size, and duration.
    Based on the response status code, different log levels (info, warning, error) are used
    to log the outcome of the request handling.

    Args:
        app (ASGIApp): The ASGI application to wrap.

    Methods:
        dispatch(request: Request, call_next: RequestResponseEndpoint) -> Response:
            Intercepts the request, logs the details, and returns the response.
            The log includes the request and response details and the time taken
            to process the request.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Process the request and log the details.

        This method measures the time taken to process the request and logs the request
        and response details such as request method, URL, size, response status, and size.
        Based on the status code of the response, the log level varies (info, warning, or error).

        Args:
            request (Request): The incoming HTTP request.
            call_next (RequestResponseEndpoint): The next ASGI application or endpoint to call.

        Returns:
            Response: The response after logging the details.
        """
        start_time = time.time()
        response = await call_next(request)
        status_code = response.status_code
        client = request.client
        end_time = f"{time.time() - start_time:.3f}s."
        extra = {
            "request_url": request.url,
            "request_method": request.method,
            "request_path": request.url.path,
            "request_size": int(request.headers.get("content-length", 0)),
            "request_host": f"{client.host}:{client.port}" if client else "",
            "response_status": status_code,
            "response_size": int(response.headers.get("content-length", 0)),
            "response_duration": end_time,
        }
        if status_code <= 299:
            logger.info("Success response", extra=extra)
        elif status_code <= 399:
            logger.info("Redirect response", extra=extra)
        elif status_code <= 499:
            logger.warning("Client request error", extra=extra)
        else:
            logger.error("Server response error", extra=extra)

        return response
