from typing import Protocol

from pydantic import UUID4


class OrganizationRepoProtocol(Protocol):
    async def check_activity_exists(self, activity: str) -> bool:
        pass

    async def get_all_organizations_from_activity(self, activity: str) -> list[str]:
        pass

    async def get_organization_by_id(self, org_id: UUID4) -> str | None:
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
