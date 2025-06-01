from typing import Protocol

from pydantic import UUID4

from app.core.models.pydantic_models import Address


class OrganizationRepoProtocol(Protocol):
    async def get_organization_id_by_name(self, org_name: str) -> UUID4 | None:
        pass

    async def get_organization_phones(self, org_id: UUID4) -> list[str]:
        pass

    async def get_organization_activities(self, org_id: UUID4) -> list[str]:
        pass

    async def get_organization_address(self, org_id: UUID4) -> Address:
        pass

    async def check_address_exists(self, address: str) -> bool:
        pass

    async def get_all_organizations_from_address(self, address: str) -> list[str]:
        pass

    async def check_activity_exists(self, activity: str) -> bool:
        pass

    async def get_all_organizations_from_activity(self, activity: str) -> list[str]:
        pass

    async def get_organization_by_id(self, org_id: UUID4) -> str | None:
        pass

    async def get_all_activities_from_ancestor(self, ancestor_name: str) -> list[str]:
        pass

    async def get_organizations_within_radius(
        self, latitude: float, longitude: float, radius: float
    ) -> list[str]:
        pass

    async def get_organization_full_info(self, org_id: UUID4) -> dict | None:
        pass

    async def get_organizations_full_info_by_names(
        self, org_names: list[str]
    ) -> list[dict]:
        pass

    async def build_address_string(self, city: str, street: str, house_num: str) -> str:
        pass

    async def get_organizations_by_address_parts(
        self, city: str, street: str, house_num: str
    ) -> list[str]:
        pass

    async def get_organizations_by_ancestor_activity_optimized(
        self, ancestor_name: str
    ) -> list[str]:
        pass

    async def get_organization_full_info_by_name(self, org_name: str) -> dict | None:
        pass
