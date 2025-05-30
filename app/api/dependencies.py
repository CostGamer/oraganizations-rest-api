from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.DB import get_db
from app.repositories.organization_repo import OrganizationRepo
from app.repositories.token_repo import TokenRepo
from app.services.organization_service import (
    GetOrganizationByIDService,
    GetOrganizationByNameService,
    GetOrganizationsFromActivityService,
    GetOrganizationsFromAddressService,
    GetOrganizationsFromAncestorActivityService,
    GetOrganizationsFromGeoService,
)
from app.services.token_service import GetApiTokensService, IssueApiTokenService


def get_token_repo(db: AsyncSession = Depends(get_db)) -> TokenRepo:
    return TokenRepo(db)


def get_organization_repo(
    db: AsyncSession = Depends(get_db),
) -> OrganizationRepo:
    return OrganizationRepo(db)


def get_issue_token_service(
    token_repo: TokenRepo = Depends(get_token_repo),
) -> IssueApiTokenService:
    return IssueApiTokenService(token_repo)


def get_api_tokens_service(
    token_repo: TokenRepo = Depends(get_token_repo),
) -> GetApiTokensService:
    return GetApiTokensService(token_repo)


def get_organization_by_name_service(
    organization_repo: OrganizationRepo = Depends(get_organization_repo),
) -> GetOrganizationByNameService:
    return GetOrganizationByNameService(organization_repo)


def get_organization_from_address(
    organization_repo: OrganizationRepo = Depends(get_organization_repo),
) -> GetOrganizationsFromAddressService:
    return GetOrganizationsFromAddressService(organization_repo)


def get_organization_from_activity(
    organization_repo: OrganizationRepo = Depends(get_organization_repo),
) -> GetOrganizationsFromActivityService:
    return GetOrganizationsFromActivityService(organization_repo)


def get_organization_from_id(
    organization_repo: OrganizationRepo = Depends(get_organization_repo),
) -> GetOrganizationByIDService:
    return GetOrganizationByIDService(organization_repo)


def get_organization_from_ancestor_acivity(
    organization_repo: OrganizationRepo = Depends(get_organization_repo),
) -> GetOrganizationsFromAncestorActivityService:
    return GetOrganizationsFromAncestorActivityService(organization_repo)


def get_organization_by_geo(
    organization_repo: OrganizationRepo = Depends(get_organization_repo),
) -> GetOrganizationsFromGeoService:
    return GetOrganizationsFromGeoService(organization_repo)
