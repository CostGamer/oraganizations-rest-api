from app.core.custom_exceptions import AlreadyManyTokensError, UserHasNoTokensError
from app.core.models.pydantic_models import ApiKey
from app.core.schemas.repo_protocols import TokenRepoProtocol

from .mixins_service import TokenMixinService


class IssueApiTokenService(TokenMixinService):
    def __init__(self, token_repo: TokenRepoProtocol) -> None:
        super().__init__(token_repo)

    async def __call__(self, login: str) -> str:
        user_exists = await self._token_repo.check_user_already_in_system(login)
        if not user_exists:
            user_id = await self._token_repo.insert_user(login)
        else:
            user_id = await self._token_repo.get_user_id(login)

        tokens_count = await self._token_repo.get_quantity_of_tokens(user_id)
        if tokens_count >= 5:
            raise AlreadyManyTokensError

        api_key = self._token_repo.generate_api_token()
        new_api_key = await self._token_repo.insert_api_token(user_id, api_key)
        return new_api_key


class GetApiTokensService(TokenMixinService):
    def __init__(self, token_repo: TokenRepoProtocol) -> None:
        super().__init__(token_repo)

    async def __call__(self, login: str) -> list[ApiKey]:
        all_tokens = await self._token_repo.get_all_tokens(login)
        if not all_tokens:
            raise UserHasNoTokensError
        return all_tokens
