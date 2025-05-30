import secrets

from pydantic import UUID4
from sqlalchemy import func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pydantic_schemas import ApiKey
from app.DB.models import ApiTokens, Users


class TokenRepo:
    def __init__(self, con: AsyncSession) -> None:
        self._con = con

    async def check_user_already_in_system(self, user_login: str) -> bool:
        """
        Returns:
            bool: True if the user is already in the system, otherwise False
        Args:
            user_login (str): The login of the user
        """
        query = select(Users).where(Users.login == user_login)
        query_res = (await self._con.execute(query)).scalar_one_or_none()
        return query_res is not None

    async def insert_user(self, user_login: str) -> UUID4:
        """
        Insert a new user into the system

        Returns:
            UUID4: The ID of the user
        Args:
            user_login (str): The login of the user
        """
        query = insert(Users).values(login=user_login).returning(Users.id)
        query_res = (await self._con.execute(query)).scalar_one()
        return query_res

    async def get_user_id(self, user_login: str) -> UUID4:
        """
        Get the ID of the existing user

        Returns:
            UUID4: The ID of the user
        Args:
            user_login (str): The login of the user
        """
        query = select(Users.id).where(Users.login == user_login)
        query_res = (await self._con.execute(query)).scalar_one()
        return query_res

    async def issuing_api_token(
        self,
    ) -> str:
        """
        Returns:
            str: The generated API key
        """
        generated_api_key = secrets.token_urlsafe(32)
        return generated_api_key

    async def insert_api_token(self, user_id: UUID4, api_key: str) -> str:
        """
        Returns:
            str: The inserted API key
        Args:
            user_id (UUID4): The ID of the user
            api_key (str): The API key
        """
        query = (
            insert(ApiTokens)
            .values(user_id=user_id, token=api_key)
            .returning(ApiTokens.token)
        )
        query_res = (await self._con.execute(query)).scalar_one()
        return query_res

    async def get_quantity_of_tokens(self, user_id: UUID4) -> int:
        """
        Returns:
            int: The quantity of tokens
        Args:
            user_id (UUID4): The ID of the user
        """
        query = select(ApiTokens).where(ApiTokens.user_id == user_id)
        query_res = (await self._con.execute(query)).scalars().all()
        return len(query_res)

    async def get_all_tokens(self, login: str) -> list[ApiKey]:
        """
        Returns:
            list[ApiKey]: A list of API keys
        Args:
            login (str): The login of the user
        """
        query = select(ApiTokens).join(Users).where(Users.login == login)
        query_res = (await self._con.execute(query)).scalars().all()
        return [ApiKey.model_validate(token_data) for token_data in query_res]

    async def update_limit(self, user_id: UUID4) -> None:
        """
        Update the limit of the tokens in an hour

        Args:
            user_id (UUID4): The ID of the user
        """
        query = update(ApiTokens).where(ApiTokens.user_id == user_id).values(limit=100)
        await self._con.execute(query)

    async def check_token_in_system(self, token: str) -> bool:
        """
        Returns:
            bool: True if the token is in the system, otherwise False
        Args:
            token (str): The token to check
        """
        query = select(ApiTokens).where(ApiTokens.token == token)
        query_res = (await self._con.execute(query)).scalar_one_or_none()
        return query_res is not None

    async def check_token_limit(self, token: str) -> tuple:
        """
        Returns:
            tuple: The limit and the last update of the token
        Args:
            token (str): The token to check limit
        """
        query = select(ApiTokens).where(ApiTokens.token == token)
        query_res = (await self._con.execute(query)).scalar_one()
        return (query_res.limit, query_res.last_update)

    async def decrese_token_limit(self, token: str) -> None:
        """
        Args:
            token (str): The token to decrease the limit
        """
        query = (
            update(ApiTokens)
            .where(ApiTokens.token == token)
            .values(limit=ApiTokens.limit - 1)
        )
        await self._con.execute(query)

    async def update_token_limit(self, token: str) -> None:
        """
        Args:
            token (str): The token to update the limit
        """
        query = update(ApiTokens).where(ApiTokens.token == token).values(limit=100)
        await self._con.execute(query)

    async def update_token_time(self, token: str) -> None:
        """
        Args:
            token (str): The token to update the time
        """
        query = (
            update(ApiTokens)
            .where(ApiTokens.token == token)
            .values(last_update=func.now())
        )
        await self._con.execute(query)
