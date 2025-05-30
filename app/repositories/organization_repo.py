from pydantic import UUID4
from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pydantic_schemas import Address
from app.DB.models import (
    Activities,
    ActivityClosure,
    Buildings,
    OrganizationActivities,
    OrganizationPhones,
    Organizations,
    Phones,
)


class OrganizationRepo:
    def __init__(self, con: AsyncSession) -> None:
        self._con = con

    async def get_organization_id_by_name(self, org_name: str) -> UUID4 | None:
        """
        Returns:
            UUID4 | None: The organization ID if found, otherwise None
        Args:
            org_name (str): The name of the organization
        """
        query = select(Organizations.id).where(Organizations.name == org_name)
        query_res = (await self._con.execute(query)).scalar_one_or_none()
        return query_res

    async def get_organization_phones(self, org_id: UUID4) -> list[str]:
        """
        Returns:
            list[str]: A list of phone numbers associated with the organization
        Args:
            org_id (UUID4): The ID of the organization
        """
        query = (
            select(Phones.phone_number)
            .join(OrganizationPhones)
            .where(OrganizationPhones.organization_id == org_id)
        )
        query_res = (await self._con.execute(query)).scalars().all()
        return list(query_res)

    async def get_organization_activities(self, org_id: UUID4) -> list[str]:
        """
        Returns:
            list[str]: The activities of the organization
        Args:
            org_id (UUID4): The ID of the organization
        """
        query = (
            select(Activities.name)
            .join(OrganizationActivities)
            .where(OrganizationActivities.organization_id == org_id)
        )
        query_res = (await self._con.execute(query)).scalars().all()
        return list(query_res)

    async def get_organization_address(self, org_id: UUID4) -> Address:
        """
        Returns:
            Address: The address of the organization
        Args:
            org_id (UUID4): The ID of the organization
        """
        query = (
            select(Buildings.address, Buildings.office)
            .join(Organizations)
            .where(Organizations.id == org_id)
        )
        query_res = (await self._con.execute(query)).one()

        address_data = {
            "address": query_res[0],
            "office": query_res[1],
        }

        return Address.model_validate(address_data)

    async def check_adress_exists(self, address: str) -> bool:
        """
        Returns:
            bool: True if the address exists, False otherwise
        Args:
            address (str): The address to check
        """
        query = select(Buildings).where(Buildings.address == address).limit(1)
        query_res = (await self._con.execute(query)).scalar_one_or_none()
        return query_res is not None

    async def get_all_organizations_from_address(self, address: str) -> list[str]:
        """
        Returns:
            list[str]: The names of the organizations in the address
        Args:
            address (str): The ID of the organizations
        """
        query = (
            select(Organizations.name)
            .join(Buildings)
            .where(Buildings.address == address)
        )
        query_res = (await self._con.execute(query)).scalars().all()
        return list(query_res)

    async def check_activity_exists(self, activity: str) -> bool:
        query = select(Activities).where(Activities.name == activity)
        query_res = (await self._con.execute(query)).scalar_one_or_none()
        return query_res is not None

    async def get_all_organizations_from_activity(self, activity: str) -> list[str]:
        query = (
            select(Organizations.name)
            .join(OrganizationActivities)
            .join(Activities)
            .where(Activities.name == activity)
        )
        query_res = (await self._con.execute(query)).scalars().all()
        return list(query_res)

    async def get_organization_by_id(self, org_id: UUID4) -> str | None:
        query = select(Organizations.name).where(Organizations.id == org_id)
        query_res = (await self._con.execute(query)).scalar_one_or_none()
        return query_res

    async def get_all_activities_from_ancestor(self, ancestor_name: str) -> list[str]:
        query = (
            select(distinct(Activities.name))
            .join(ActivityClosure, ActivityClosure.descendant_id == Activities.id)
            .where(
                ActivityClosure.ancestor_id
                == (select(Activities.id).where(Activities.name == ancestor_name))
            )
        )
        query_res = (await self._con.execute(query)).scalars().all()
        return list(query_res)

    async def get_organizations_within_radius(
        self, latitude: float, longitude: float, radius: float
    ) -> list[str]:
        query = (
            select(Organizations.name)
            .join(Buildings)
            .where(
                func.ST_DWithin(
                    Buildings.location,
                    func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326),
                    radius,
                )
            )
        )
        result = (await self._con.execute(query)).scalars().all()
        return list(result)
