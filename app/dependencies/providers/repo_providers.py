from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas.repo_protocols import OrganizationRepoProtocol, TokenRepoProtocol
from app.repositories import OrganizationRepo, TokenRepo


class RepoProviders(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_token_repo(self, con: AsyncSession) -> TokenRepoProtocol:
        return TokenRepo(con)

    @provide(scope=Scope.REQUEST)
    async def get_organization_repo(
        self, con: AsyncSession
    ) -> OrganizationRepoProtocol:
        return OrganizationRepo(con)
