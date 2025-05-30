from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core import all_settings
from app.DB.db import get_session

get_session_instance = get_session(all_settings.database)


async def get_db() -> AsyncIterator[AsyncSession]:
    async for session in get_session_instance():
        yield session
