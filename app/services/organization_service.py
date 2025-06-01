from pydantic import UUID4

from app.core.custom_exceptions import (
    ActivityNotFoundError,
    AddressNotFoundError,
    OrganizationNotFoundError,
)
from app.core.models.pydantic_models import Address, Organization
from app.core.schemas.repo_protocols import OrganizationRepoProtocol
from app.services.mixins_service import OrganizationMixinService


class OrganizationCommonService(OrganizationMixinService):
    def __init__(self, organization_repo: OrganizationRepoProtocol) -> None:
        super().__init__(organization_repo)

    async def get_organization_by_name(self, name: str) -> Organization:
        org_info = await self._organization_repo.get_organization_full_info_by_name(
            name
        )
        if not org_info:
            raise OrganizationNotFoundError

        address = Address(address=org_info["address"] or "", office=org_info["office"])

        return Organization(
            name=org_info["name"],
            phones_numbers=org_info["phones"],
            address=address,
            activities=org_info["activities"],
        )

    def _create_organizations_from_dict_list(
        self, org_data_list: list[dict]
    ) -> list[Organization]:
        organizations = []

        for org_data in org_data_list:
            address = Address(
                address=org_data["address"] or "", office=org_data["office"]
            )

            organization = Organization(
                name=org_data["name"],
                phones_numbers=org_data["phones"],
                address=address,
                activities=org_data["activities"],
            )
            organizations.append(organization)

        return organizations


class GetOrganizationByNameService(OrganizationCommonService):
    def __init__(self, organization_repo: OrganizationRepoProtocol) -> None:
        super().__init__(organization_repo)

    async def __call__(self, name: str) -> Organization:
        return await self.get_organization_by_name(name)


class GetOrganizationsFromAddressService(OrganizationCommonService):
    def __init__(self, organization_repo: OrganizationRepoProtocol) -> None:
        super().__init__(organization_repo)

    async def __call__(
        self, city: str, street: str, house_num: str
    ) -> list[Organization]:
        organization_names = (
            await self._organization_repo.get_organizations_by_address_parts(
                city, street, house_num
            )
        )

        if not organization_names:
            raise AddressNotFoundError

        org_data_list = (
            await self._organization_repo.get_organizations_full_info_by_names(
                organization_names
            )
        )

        return self._create_organizations_from_dict_list(org_data_list)


class GetOrganizationsFromActivityService(OrganizationCommonService):
    def __init__(self, organization_repo: OrganizationRepoProtocol) -> None:
        super().__init__(organization_repo)

    async def __call__(self, activity: str) -> list[Organization]:
        if not await self._organization_repo.check_activity_exists(activity):
            raise ActivityNotFoundError

        organization_names = (
            await self._organization_repo.get_all_organizations_from_activity(activity)
        )

        if not organization_names:
            return []

        org_data_list = (
            await self._organization_repo.get_organizations_full_info_by_names(
                organization_names
            )
        )

        return self._create_organizations_from_dict_list(org_data_list)


class GetOrganizationByIDService:
    def __init__(self, organization_repo: OrganizationRepoProtocol) -> None:
        self._organization_repo = organization_repo

    async def __call__(self, org_id: UUID4) -> Organization:
        org_info = await self._organization_repo.get_organization_full_info(org_id)
        if not org_info:
            raise OrganizationNotFoundError

        address = Address(address=org_info["address"] or "", office=org_info["office"])

        return Organization(
            name=org_info["name"],
            phones_numbers=org_info["phones"],
            address=address,
            activities=org_info["activities"],
        )


class GetOrganizationsFromAncestorActivityService(OrganizationCommonService):
    def __init__(self, organization_repo: OrganizationRepoProtocol) -> None:
        super().__init__(organization_repo)

    async def __call__(self, activity: str) -> list[Organization]:
        if not await self._organization_repo.check_activity_exists(activity):
            raise ActivityNotFoundError

        organization_names = await self._organization_repo.get_organizations_by_ancestor_activity_optimized(
            activity
        )

        if not organization_names:
            return []

        org_data_list = (
            await self._organization_repo.get_organizations_full_info_by_names(
                organization_names
            )
        )

        return self._create_organizations_from_dict_list(org_data_list)


class GetOrganizationsFromGeoService(OrganizationCommonService):
    def __init__(self, organization_repo: OrganizationRepoProtocol) -> None:
        super().__init__(organization_repo)

    async def __call__(
        self, latitude: float, longitude: float, radius: float
    ) -> list[Organization]:
        organization_names = (
            await self._organization_repo.get_organizations_within_radius(
                latitude, longitude, radius
            )
        )

        if not organization_names:
            return []

        org_data_list = (
            await self._organization_repo.get_organizations_full_info_by_names(
                organization_names
            )
        )

        return self._create_organizations_from_dict_list(org_data_list)
