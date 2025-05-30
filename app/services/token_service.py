from app.core.custom_exceptions import AlreadyManyTokensError, UserHasNoTokensError
from app.core.pydantic_schemas import ApiKey
from app.repositories.token_repo import TokenRepo


class IssueApiTokenService:
    """Service for issuing API tokens to users.

    This service manages the issuance of API tokens for a user.
    It ensures that a user is registered in the system and restricts the
    number of tokens that can be issued to a single user.

    Args:
        token_repo (TokenRepo): Repository for token management and user interactions.

    Methods:
        __call__(login: str) -> str:
            Issues a new API token for the given login. If the user does not exist,
            they are registered. Raises an exception if the user already has the maximum
            number of tokens.
    """

    def __init__(
        self,
        token_repo: TokenRepo,
    ) -> None:
        self._token_repo = token_repo

    async def __call__(self, login: str) -> str:
        """Issues a new API token for the given login.

        Args:
            login (str): The login of the user requesting a token.

        Returns:
            str: The newly issued API token.

        Raises:
            AlreadyManyTokensError: If the user already has the maximum number of tokens.
        """
        check_user_already_in_system = (
            await self._token_repo.check_user_already_in_system(login)
        )
        if not check_user_already_in_system:
            user_id = await self._token_repo.insert_user(login)
        else:
            user_id = await self._token_repo.get_user_id(login)

        get_quantity_of_tokens = await self._token_repo.get_quantity_of_tokens(user_id)
        if get_quantity_of_tokens >= 5:
            raise AlreadyManyTokensError

        api_key = await self._token_repo.issuing_api_token()
        new_api_key = await self._token_repo.insert_api_token(user_id, api_key)

        return new_api_key


class GetApiTokensService:
    """Service for retrieving all API tokens associated with a user.

    This service fetches all API tokens linked to a user's account. If no tokens are
    found, an exception is raised.

    Args:
        token_repo (TokenRepo): Repository for token management and user interactions.

    Methods:
        __call__(login: str) -> list[ApiKey]:
            Retrieves all API tokens for the given login. Raises an exception
            if the user has no tokens.
    """

    def __init__(
        self,
        token_repo: TokenRepo,
    ) -> None:
        self._token_repo = token_repo

    async def __call__(self, login: str) -> list[ApiKey]:
        """Retrieves all API tokens for the given login.

        Args:
            login (str): The login of the user whose tokens are being requested.

        Returns:
            list[ApiKey]: A list of API tokens associated with the user.

        Raises:
            UserHasNoTokensError: If the user has no tokens in the system.
        """
        all_tokens = await self._token_repo.get_all_tokens(login)
        if len(all_tokens) == 0:
            raise UserHasNoTokensError
        return all_tokens
