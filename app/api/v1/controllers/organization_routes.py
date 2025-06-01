from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter
from pydantic import UUID4

from app.api.exception_responses.responses import (
    get_organization_by_id_geo_responses,
    get_organization_by_name_responses,
    get_organizations_by_activity_responses,
    get_organizations_by_address_responses,
)
from app.core.models.pydantic_models import Organization
from app.core.schemas.service_protocols import (
    GetOrganizationByIDServiceProtocol,
    GetOrganizationByNameServiceProtocol,
    GetOrganizationsFromActivityServiceProtocol,
    GetOrganizationsFromAddressServiceProtocol,
    GetOrganizationsFromAncestorActivityServiceProtocol,
    GetOrganizationsFromGeoServiceProtocol,
)

organization_router = APIRouter()


@organization_router.get(
    "/name",
    response_model=Organization,
    responses=get_organization_by_name_responses,
    description="endpoint for getting organization by name",
)
@inject
async def get_organization_by_name(
    name: str,
    organization_by_name_service: FromDishka[GetOrganizationByNameServiceProtocol],
) -> Organization:
    return await organization_by_name_service(name)


@organization_router.get(
    "/address",
    response_model=list[Organization],
    responses=get_organizations_by_address_responses,
    description="endpoint for getting organizations by address",
)
@inject
async def get_organizations_by_address(
    city: str,
    street: str,
    house_num: str,
    organizations_from_adress_service: FromDishka[
        GetOrganizationsFromAddressServiceProtocol
    ],
) -> list[Organization]:
    return await organizations_from_adress_service(city, street, house_num)


@organization_router.get(
    "/activity",
    response_model=list[Organization],
    responses=get_organizations_by_activity_responses,
    description="endpoint for getting organizations by activity",
)
@inject
async def get_organizations_by_activity(
    activity: str,
    organizations_from_activity_service: FromDishka[
        GetOrganizationsFromActivityServiceProtocol
    ],
) -> list[Organization]:
    return await organizations_from_activity_service(activity)


@organization_router.get(
    "/id",
    response_model=Organization,
    responses=get_organization_by_id_geo_responses,
    description="endpoint for getting organization by id",
)
@inject
async def get_organization_by_id(
    org_id: UUID4,
    organization_from_id_service: FromDishka[GetOrganizationByIDServiceProtocol],
) -> Organization:
    return await organization_from_id_service(org_id)


@organization_router.get(
    "/ancestor/activity",
    response_model=list[Organization],
    responses=get_organizations_by_activity_responses,
    description="endpoint for getting organizations by ancestor activity",
)
@inject
async def get_organizations_by_ancestor_activity(
    activity: str,
    organizations_from_ancestor_activity_service: FromDishka[
        GetOrganizationsFromAncestorActivityServiceProtocol
    ],
) -> list[Organization]:
    return await organizations_from_ancestor_activity_service(activity)


@organization_router.get(
    "/location",
    response_model=list[Organization],
    responses=get_organization_by_id_geo_responses,
    description="endpoint for getting organizations by geo location",
)
@inject
async def get_organizations_by_geo_location(
    latitute: float,
    longitude: float,
    radius: float,
    organizations_from_geo_service: FromDishka[GetOrganizationsFromGeoServiceProtocol],
) -> list[Organization]:
    return await organizations_from_geo_service(latitute, longitude, radius)
