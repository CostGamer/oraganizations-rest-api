from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.core.custom_exceptions import MissingOrBadTokenError, TheLimitExceededError
from app.repositories.token_repo import TokenRepo


class CheckTokenMiddleware(BaseHTTPMiddleware):
    """Middleware to check the validity of the token in incoming requests.

    This middleware ensures that requests have a valid authorization token in the
    'Authorization' header. It checks the token's existence, validity, and the
    associated request limit. If the token is invalid or missing, or if the
    request limit is exceeded, an appropriate error response is returned.

    Excluded paths such as '/docs', '/openapi.json' and '/api_token' are
    bypassed, meaning the token validation is not applied to these routes.
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.excluded_paths = ["/docs", "/openapi.json", "/api_token"]

    async def dispatch(self, request: Request, call_next: Any) -> Any:
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

            # Получаем db_connection из состояния приложения
            db_connection = request.app.state.db_connection

            async with db_connection.get_session() as session:
                token_repo = TokenRepo(session)

                token_info = await token_repo.get_token_info_for_validation(token)
                if not token_info:
                    raise MissingOrBadTokenError

                token_limit, token_last_update = token_info
                current_time = datetime.now(timezone.utc)

                if token_last_update:
                    if isinstance(token_last_update, str):
                        last_update_time = datetime.fromisoformat(
                            token_last_update
                        ).replace(tzinfo=timezone.utc)
                    else:
                        last_update_time = (
                            token_last_update.replace(tzinfo=timezone.utc)
                            if token_last_update.tzinfo is None
                            else token_last_update
                        )
                else:
                    last_update_time = current_time - timedelta(hours=2)

                if current_time - last_update_time > timedelta(hours=1):
                    await token_repo.reset_token_limit_and_decrease(token)
                elif token_limit <= 0:
                    raise TheLimitExceededError
                else:
                    await token_repo.decrease_token_limit(token)

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
        except Exception:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal server error"},
            )

        response = await call_next(request)
        return response
