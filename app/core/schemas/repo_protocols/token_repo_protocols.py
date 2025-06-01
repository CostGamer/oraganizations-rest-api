from datetime import datetime
from typing import Optional, Protocol

from pydantic import UUID4

from app.core.models.pydantic_models import ApiKey


class TokenRepoProtocol(Protocol):
    async def check_user_already_in_system(self, user_login: str) -> bool:
        pass

    async def insert_user(self, user_login: str) -> UUID4:
        pass

    async def get_user_id(self, user_login: str) -> UUID4:
        pass

    def generate_api_token(self) -> str:
        pass

    async def insert_api_token(self, user_id: UUID4, api_key: str) -> str:
        pass

    async def get_quantity_of_tokens(self, user_id: UUID4) -> int:
        pass

    async def get_all_tokens(self, login: str) -> list[ApiKey]:
        pass

    async def update_limit(self, user_id: UUID4, limit: int = 100) -> None:
        pass

    async def check_token_in_system(self, token: str) -> bool:
        pass

    async def check_token_limit(self, token: str) -> tuple:
        pass

    async def get_token_info_for_validation(
        self, token: str
    ) -> Optional[tuple[int, datetime]]:
        pass

    async def decrease_token_limit(self, token: str) -> None:
        pass

    async def update_token_limit(self, token: str, limit: int = 100) -> None:
        pass

    async def update_token_time(self, token: str) -> None:
        pass

    async def reset_token_limit_and_decrease(
        self, token: str, limit: int = 100
    ) -> None:
        pass

    async def update_token_limit_and_time(self, token: str, limit: int = 100) -> None:
        pass
