from dishka import Provider, Scope, provide

from app.core.schemas.repo_protocols import OrganizationRepoProtocol, TokenRepoProtocol
from app.core.schemas.service_protocols import (
    GetApiTokensServiceProtocol,
    GetOrganizationByIDServiceProtocol,
    GetOrganizationByNameServiceProtocol,
    GetOrganizationsFromActivityServiceProtocol,
    GetOrganizationsFromAddressServiceProtocol,
    GetOrganizationsFromAncestorActivityServiceProtocol,
    GetOrganizationsFromGeoServiceProtocol,
    IssueApiTokenServiceProtocol,
)
from app.services import (
    GetApiTokensService,
    GetOrganizationByIDService,
    GetOrganizationByNameService,
    GetOrganizationsFromActivityService,
    GetOrganizationsFromAddressService,
    GetOrganizationsFromAncestorActivityService,
    GetOrganizationsFromGeoService,
    IssueApiTokenService,
)


class ServiceProviders(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_issue_api_token_service(
        self, token_repo: TokenRepoProtocol
    ) -> IssueApiTokenServiceProtocol:
        return IssueApiTokenService(token_repo)

    @provide(scope=Scope.REQUEST)
    async def get_api_tokens_service(
        self, token_repo: TokenRepoProtocol
    ) -> GetApiTokensServiceProtocol:
        return GetApiTokensService(token_repo)

    @provide(scope=Scope.REQUEST)
    async def get_get_organization_by_name_service(
        self, organization_repo: OrganizationRepoProtocol
    ) -> GetOrganizationByNameServiceProtocol:
        return GetOrganizationByNameService(organization_repo)

    @provide(scope=Scope.REQUEST)
    async def get_organizations_from_address_service(
        self, organization_repo: OrganizationRepoProtocol
    ) -> GetOrganizationsFromAddressServiceProtocol:
        return GetOrganizationsFromAddressService(organization_repo)

    @provide(scope=Scope.REQUEST)
    async def get_organizations_from_activity_service(
        self, organization_repo: OrganizationRepoProtocol
    ) -> GetOrganizationsFromActivityServiceProtocol:
        return GetOrganizationsFromActivityService(organization_repo)

    @provide(scope=Scope.REQUEST)
    async def get_organization_by_id_service(
        self, organization_repo: OrganizationRepoProtocol
    ) -> GetOrganizationByIDServiceProtocol:
        return GetOrganizationByIDService(organization_repo)

    @provide(scope=Scope.REQUEST)
    async def get_organizations_from_ancestor_activity_service(
        self, organization_repo: OrganizationRepoProtocol
    ) -> GetOrganizationsFromAncestorActivityServiceProtocol:
        return GetOrganizationsFromAncestorActivityService(organization_repo)

    @provide(scope=Scope.REQUEST)
    async def get_organizations_from_geo_service(
        self, organization_repo: OrganizationRepoProtocol
    ) -> GetOrganizationsFromGeoServiceProtocol:
        return GetOrganizationsFromGeoService(organization_repo)
