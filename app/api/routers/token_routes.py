from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_api_tokens_service, get_issue_token_service
from app.api.responses import get_all_tokens_responses, issue_token_responses
from app.core.pydantic_schemas import ApiKey
from app.services.token_service import GetApiTokensService, IssueApiTokenService

token_router = APIRouter()


@token_router.post(
    "/issue_token",
    response_model=str,
    responses=issue_token_responses,
    description="endpoint for issuing a new token",
)
async def issue_token(
    login: str = Query("login"),
    issue_token_service: IssueApiTokenService = Depends(get_issue_token_service),
) -> str:
    return await issue_token_service(login)


@token_router.get(
    "/get_all_tokens",
    response_model=list[ApiKey],
    responses=get_all_tokens_responses,
    description="endpoint for getting all user tokens",
)
async def get_all_tokens(
    login: str = Query("login"),
    get_api_tokens_service: GetApiTokensService = Depends(get_api_tokens_service),
) -> list[ApiKey]:
    return await get_api_tokens_service(login)
