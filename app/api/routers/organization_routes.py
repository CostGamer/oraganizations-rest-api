from fastapi import APIRouter, Depends, Query
from pydantic import UUID4

from app.api.dependencies import (
    get_organization_by_geo,
    get_organization_by_name_service,
    get_organization_from_activity,
    get_organization_from_address,
    get_organization_from_ancestor_acivity,
    get_organization_from_id,
)
from app.api.responses import (
    get_organization_by_id_geo_responses,
    get_organization_by_name_responses,
    get_organizations_by_activity_responses,
    get_organizations_by_address_responses,
)
from app.core.pydantic_schemas import Organization
from app.services.organization_service import (
    GetOrganizationByIDService,
    GetOrganizationByNameService,
    GetOrganizationsFromActivityService,
    GetOrganizationsFromAddressService,
    GetOrganizationsFromAncestorActivityService,
    GetOrganizationsFromGeoService,
)

organization_router = APIRouter()


@organization_router.get(
    "/get_organization_by_name",
    response_model=Organization,
    responses=get_organization_by_name_responses,
    description="endpoint for getting organization by name",
)
async def get_organization_by_name(
    name: str = Query("ООО Рога и Копыта"),
    organization_by_name_service: GetOrganizationByNameService = Depends(
        get_organization_by_name_service
    ),
) -> Organization:
    return await organization_by_name_service(name)


@organization_router.get(
    "/get_organizations_by_address",
    response_model=list[Organization],
    responses=get_organizations_by_address_responses,
    description="endpoint for getting organizations by address",
)
async def get_organizations_by_address(
    city: str = Query("Москва"),
    street: str = Query("Ленина"),
    house_num: str = Query("1"),
    organizations_from_adress_service: GetOrganizationsFromAddressService = Depends(
        get_organization_from_address
    ),
) -> list[Organization]:
    return await organizations_from_adress_service(city, street, house_num)


@organization_router.get(
    "/get_organizations_by_activity",
    response_model=list[Organization],
    responses=get_organizations_by_activity_responses,
    description="endpoint for getting organizations by activity",
)
async def get_organizations_by_activity(
    activity: str = Query("Еда"),
    organizations_from_activity_service: GetOrganizationsFromActivityService = Depends(
        get_organization_from_activity
    ),
) -> list[Organization]:
    return await organizations_from_activity_service(activity)


@organization_router.get(
    "/get_organization_by_id",
    response_model=Organization,
    responses=get_organization_by_id_geo_responses,
    description="endpoint for getting organization by id",
)
async def get_organization_by_id(
    org_id: UUID4,
    organization_from_id_service: GetOrganizationByIDService = Depends(
        get_organization_from_id
    ),
) -> Organization:
    return await organization_from_id_service(org_id)


@organization_router.get(
    "/get_organizations_by_ancestor_activity",
    response_model=list[Organization],
    responses=get_organizations_by_activity_responses,
    description="endpoint for getting organizations by ancestor activity",
)
async def get_organizations_by_ancestor_activity(
    activity: str = Query("Еда"),
    organizations_from_ancestor_activity_service: GetOrganizationsFromAncestorActivityService = Depends(
        get_organization_from_ancestor_acivity
    ),
) -> list[Organization]:
    return await organizations_from_ancestor_activity_service(activity)


@organization_router.get(
    "/get_organizations_by_geo_location",
    response_model=list[Organization],
    responses=get_organization_by_id_geo_responses,
    description="endpoint for getting organizations by geo location",
)
async def get_organizations_by_geo_location(
    latitute: float = Query(55.7558),
    longitude: float = Query(37.6176),
    radius: float = Query(1000),
    organizations_from_geo_service: GetOrganizationsFromGeoService = Depends(
        get_organization_by_geo
    ),
) -> list[Organization]:
    return await organizations_from_geo_service(latitute, longitude, radius)
