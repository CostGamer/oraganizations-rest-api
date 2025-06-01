from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from app.api.exception_responses.responses import (
    get_all_tokens_responses,
    issue_token_responses,
)
from app.core.models.pydantic_models import ApiKey
from app.core.schemas.service_protocols import (
    GetApiTokensServiceProtocol,
    IssueApiTokenServiceProtocol,
)

token_router = APIRouter()


@token_router.post(
    "/issue",
    response_model=str,
    responses=issue_token_responses,
    description="endpoint for issuing a new token",
)
@inject
async def issue_token(
    login: str,
    issue_token_service: FromDishka[IssueApiTokenServiceProtocol],
) -> str:
    return await issue_token_service(login)


@token_router.get(
    "/tokens",
    response_model=list[ApiKey],
    responses=get_all_tokens_responses,
    description="endpoint for getting all user tokens",
)
@inject
async def get_all_tokens(
    login: str,
    get_api_tokens_service: FromDishka[GetApiTokensServiceProtocol],
) -> list[ApiKey]:
    return await get_api_tokens_service(login)
