import random
import string
from collections.abc import AsyncIterator
from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.configs import all_settings
from app.main import setup_app


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    app = setup_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac


@pytest.fixture(scope="session")
async def async_engine() -> AsyncIterator[AsyncEngine]:
    engine = create_async_engine(
        all_settings.database.db_uri, echo=True, future=True, poolclass=NullPool
    )
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
async def register_token(async_client: AsyncClient) -> AsyncGenerator[str, None]:
    random_login = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(10)
    )
    token_issue_data = {"login": random_login}

    login_response = await async_client.post(
        "/api_token/issue", params=token_issue_data
    )

    assert login_response.status_code == 200, (
        f"Unexpected status code: {login_response.status_code}. "
        f"Response: {login_response.text}"
    )

    yield random_login


@pytest.fixture(scope="session")
async def authenticated_token(
    async_client: AsyncClient, register_token: str
) -> AsyncGenerator[str, None]:
    login_response = await async_client.get(
        "/api_token/tokens", params={"login": register_token}
    )

    assert login_response.status_code == 200, (
        f"Unexpected status code: {login_response.status_code}. "
        f"Response: {login_response.text}"
    )

    response_json = login_response.json()

    assert response_json, "No tokens found in response"

    api_key_token = response_json[0].get("token")
    assert api_key_token, "API key token not found in response"

    yield api_key_token


@pytest.fixture(scope="session", autouse=True)
async def set_auth_headers(
    async_client: AsyncClient, authenticated_token: str
) -> AsyncGenerator[AsyncClient, None]:
    async_client.headers.update({"Authorization": f"Bearer {authenticated_token}"})
    yield async_client
