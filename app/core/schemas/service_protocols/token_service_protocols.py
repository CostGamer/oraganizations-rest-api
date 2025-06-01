from typing import Protocol

from app.core.models.pydantic_models import ApiKey


class IssueApiTokenServiceProtocol(Protocol):
    async def __call__(self, login: str) -> str:
        pass


class GetApiTokensServiceProtocol(Protocol):
    async def __call__(self, login: str) -> list[ApiKey]:
        pass
