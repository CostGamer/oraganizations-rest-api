from app.core.schemas.repo_protocols import OrganizationRepoProtocol, TokenRepoProtocol


class TokenMixinService:
    def __init__(self, token_repo: TokenRepoProtocol) -> None:
        self._token_repo = token_repo


class OrganizationMixinService:
    def __init__(self, organization_repo: OrganizationRepoProtocol) -> None:
        self._organization_repo = organization_repo
