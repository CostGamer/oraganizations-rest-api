from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.custom_exceptions import (
    AddressNotFoundError,
    AlreadyManyTokensError,
    OrganizationNotFoundError,
    UserHasNoTokensError,
)


async def many_tokens_error(
    request: Request, exc: AlreadyManyTokensError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": "This user already has 5 tokens, use the /get_all_tokens endpoint to get all tokens"
        },
    )


async def user_has_no_tokens_error(
    request: Request, exc: UserHasNoTokensError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": "User has no tokens, use the /issue_token endpoint to issue a new token"
        },
    )


async def organization_not_exists_error(
    request: Request, exc: OrganizationNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "This organization does not exist"},
    )


async def address_not_exists_error(
    request: Request, exc: AddressNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "This address does not exist"},
    )
