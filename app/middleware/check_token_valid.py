from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.api.dependencies import get_token_repo
from app.core.custom_exceptions import MissingOrBadTokenError, TheLimitExceededError
from app.DB import get_db


class CheckTokenMiddleware(BaseHTTPMiddleware):
    """Middleware to check the validity of the token in incoming requests.

    This middleware ensures that requests have a valid authorization token in the
    'Authorization' header. It checks the token's existence, validity, and the
    associated request limit. If the token is invalid or missing, or if the
    request limit is exceeded, an appropriate error response is returned.

    Excluded paths such as '/docs', '/openapi.json' and '/api_token' are
    bypassed, meaning the token validation is not applied to these routes.

    Args:
        app (ASGIApp): The ASGI application to wrap.

    Attributes:
        excluded_paths (list): A list of paths that are excluded from token validation.

    Methods:
        dispatch(request: Request, call_next: Any) -> Any:
            Intercepts the request and checks the validity of the token. If the token
            is invalid or has exceeded its limit, an error response is returned.
            Otherwise, it proceeds with the request and returns the response.
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.excluded_paths = ["/docs", "/openapi.json", "/api_token"]

    async def dispatch(self, request: Request, call_next: Any) -> Any:
        """Processes the request and checks the token validity.

        This method checks if the token is included in the 'Authorization' header,
        validates the token, and checks its usage limit. If the token is missing or
        invalid, or if the request limit has been exceeded, an appropriate error response
        is returned.

        Args:
            request (Request): The incoming request.
            call_next (Any): The next ASGI application to call.

        Returns:
            JSONResponse: A response indicating the result of token validation or
            the original response if validation is successful.
        """
        try:
            if any(
                request.url.path.startswith(path.rstrip("/"))
                for path in self.excluded_paths
            ):
                return await call_next(request)

            token = request.headers.get("Authorization")
            if not token or not token.startswith("Bearer "):
                raise MissingOrBadTokenError
            token = token.split(" ", 1)[1]

            async for db in get_db():
                token_repo = get_token_repo(db)

                check_token_in_system = await token_repo.check_token_in_system(token)
                if not check_token_in_system:
                    raise MissingOrBadTokenError

                token_limit, token_last_update = await token_repo.check_token_limit(
                    token
                )

                current_time = datetime.now(timezone.utc)
                iso_token_last_update = datetime.fromisoformat(
                    str(token_last_update)
                ).replace(tzinfo=timezone.utc)
                if current_time - iso_token_last_update > timedelta(hours=1):
                    await token_repo.update_token_limit(token)
                    await token_repo.decrese_token_limit(token)
                    await token_repo.update_token_time(token)
                elif token_limit == 0:
                    raise TheLimitExceededError
                else:
                    await token_repo.decrese_token_limit(token)
        except MissingOrBadTokenError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "The token is missing or bad"},
            )
        except TheLimitExceededError:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "The limit of requests exceeded"},
            )

        response = await call_next(request)
        return response
