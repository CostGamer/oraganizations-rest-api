import secrets
from datetime import datetime
from typing import Optional

from pydantic import UUID4
from sqlalchemy import func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.pydantic_models import ApiKey
from app.core.models.sqlalchemy_models import ApiTokens, Users


class TokenRepo:
    def __init__(self, con: AsyncSession) -> None:
        self._con = con

    async def check_user_already_in_system(self, user_login: str) -> bool:
        query = select(Users.id).where(Users.login == user_login)
        query_res = (await self._con.execute(query)).scalar_one_or_none()
        return query_res is not None

    async def insert_user(self, user_login: str) -> UUID4:
        query = insert(Users).values(login=user_login).returning(Users.id)
        query_res = (await self._con.execute(query)).scalar_one()
        return query_res

    async def get_user_id(self, user_login: str) -> UUID4:
        query = select(Users.id).where(Users.login == user_login)
        query_res = (await self._con.execute(query)).scalar_one()
        return query_res

    def generate_api_token(self) -> str:
        return secrets.token_urlsafe(32)

    async def insert_api_token(self, user_id: UUID4, api_key: str) -> str:
        query = (
            insert(ApiTokens)
            .values(user_id=user_id, token=api_key)
            .returning(ApiTokens.token)
        )
        query_res = (await self._con.execute(query)).scalar_one()
        return query_res

    async def get_quantity_of_tokens(self, user_id: UUID4) -> int:
        query = select(func.count(ApiTokens.id)).where(ApiTokens.user_id == user_id)
        query_res = (await self._con.execute(query)).scalar_one()
        return query_res

    async def get_all_tokens(self, login: str) -> list[ApiKey]:
        query = select(ApiTokens).join(Users).where(Users.login == login)
        query_res = (await self._con.execute(query)).scalars().all()
        return [ApiKey.model_validate(token_data) for token_data in query_res]

    async def get_token_info_for_validation(
        self, token: str
    ) -> Optional[tuple[int, datetime]]:
        query = select(ApiTokens.limit, ApiTokens.last_update).where(
            ApiTokens.token == token
        )
        query_res = (await self._con.execute(query)).first()
        return (query_res.limit, query_res.last_update) if query_res else None

    async def decrease_token_limit(self, token: str) -> None:
        query = (
            update(ApiTokens)
            .where(ApiTokens.token == token)
            .values(limit=ApiTokens.limit - 1)
        )
        await self._con.execute(query)

    async def reset_token_limit_and_decrease(
        self, token: str, limit: int = 100
    ) -> None:
        query = (
            update(ApiTokens)
            .where(ApiTokens.token == token)
            .values(limit=limit - 1, last_update=func.now())
        )
        await self._con.execute(query)
