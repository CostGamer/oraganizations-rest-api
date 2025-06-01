from logging import getLogger

from dishka.integrations.fastapi import setup_dishka
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

from app.api.exception_responses.exceptions import (
    address_not_exists_error,
    many_tokens_error,
    organization_not_exists_error,
    user_has_no_tokens_error,
)
from app.api.v1.controllers import organization_router, token_router
from app.core.configs import all_settings, db_connection
from app.core.custom_exceptions import (
    AddressNotFoundError,
    AlreadyManyTokensError,
    OrganizationNotFoundError,
    UserHasNoTokensError,
)
from app.core.utils import init_logger
from app.dependencies.container import container
from app.middleware.check_token_valid import CheckTokenMiddleware
from app.middleware.logger import LoggerMiddleware

logger = getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AlreadyManyTokensError, many_tokens_error)  # type: ignore
    app.add_exception_handler(UserHasNoTokensError, user_has_no_tokens_error)  # type: ignore
    app.add_exception_handler(OrganizationNotFoundError, organization_not_exists_error)  # type: ignore
    app.add_exception_handler(AddressNotFoundError, address_not_exists_error)  # type: ignore


def init_routers(app: FastAPI) -> None:
    http_bearer = HTTPBearer(auto_error=True)
    app.include_router(token_router, prefix="/api_token", tags=["api_token"])
    app.include_router(
        organization_router,
        prefix="/organization",
        tags=["organization"],
        dependencies=[Depends(http_bearer)],
    )


def init_middlewares(app: FastAPI) -> None:
    origins = all_settings.different.list_of_origins

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(LoggerMiddleware)
    app.add_middleware(CheckTokenMiddleware)


def setup_app() -> FastAPI:
    app = FastAPI(
        title="Organizations Directory API",
        description="API for working with data on organizations, buildings, and activities. \
                    Supports location-based search, activity classification, and advanced filtering",
        version="0.1.0",
    )
    app.state.db_connection = db_connection
    init_logger(all_settings.logging)
    setup_dishka(app=app, container=container)
    init_routers(app)
    init_middlewares(app)
    register_exception_handlers(app)
    logger.info("App created", extra={"app_version": app.version})
    return app
