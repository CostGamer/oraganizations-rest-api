from pydantic import UUID4
from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.pydantic_models import Address
from app.core.models.sqlalchemy_models import (
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
        query = select(Organizations.id).where(Organizations.name == org_name)
        query_res = (await self._con.execute(query)).scalar_one_or_none()
        return query_res

    async def get_organization_phones(self, org_id: UUID4) -> list[str]:
        query = (
            select(Phones.phone_number)
            .join(OrganizationPhones)
            .where(OrganizationPhones.organization_id == org_id)
        )
        query_res = (await self._con.execute(query)).scalars().all()
        return list(query_res)

    async def get_organization_activities(self, org_id: UUID4) -> list[str]:
        query = (
            select(Activities.name)
            .join(OrganizationActivities)
            .where(OrganizationActivities.organization_id == org_id)
        )
        query_res = (await self._con.execute(query)).scalars().all()
        return list(query_res)

    async def get_organization_address(self, org_id: UUID4) -> Address:
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

    async def check_address_exists(self, address: str) -> bool:
        query = select(Buildings.id).where(Buildings.address == address).limit(1)
        query_res = (await self._con.execute(query)).scalar_one_or_none()
        return query_res is not None

    async def get_all_organizations_from_address(self, address: str) -> list[str]:
        query = (
            select(Organizations.name)
            .join(Buildings)
            .where(Buildings.address == address)
        )
        query_res = (await self._con.execute(query)).scalars().all()
        return list(query_res)

    async def check_activity_exists(self, activity: str) -> bool:
        query = select(Activities.id).where(Activities.name == activity).limit(1)
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

    async def get_organization_full_info(self, org_id: UUID4) -> dict | None:
        query = (
            select(
                Organizations.name,
                Buildings.address,
                Buildings.office,
                func.array_agg(distinct(Phones.phone_number)).label("phones"),
                func.array_agg(distinct(Activities.name)).label("activities"),
            )
            .select_from(Organizations)
            .join(Buildings, isouter=True)
            .join(OrganizationPhones, isouter=True)
            .join(Phones, isouter=True)
            .join(OrganizationActivities, isouter=True)
            .join(Activities, isouter=True)
            .where(Organizations.id == org_id)
            .group_by(Organizations.name, Buildings.address, Buildings.office)
        )

        result = (await self._con.execute(query)).first()
        if not result:
            return None

        return {
            "name": result.name,
            "address": result.address,
            "office": result.office,
            "phones": [p for p in result.phones if p is not None],
            "activities": [a for a in result.activities if a is not None],
        }

    async def get_organizations_full_info_by_names(
        self, org_names: list[str]
    ) -> list[dict]:
        if not org_names:
            return []

        query = (
            select(
                Organizations.id,
                Organizations.name,
                Buildings.address,
                Buildings.office,
                func.array_agg(distinct(Phones.phone_number)).label("phones"),
                func.array_agg(distinct(Activities.name)).label("activities"),
            )
            .select_from(Organizations)
            .join(Buildings, isouter=True)
            .join(OrganizationPhones, isouter=True)
            .join(Phones, isouter=True)
            .join(OrganizationActivities, isouter=True)
            .join(Activities, isouter=True)
            .where(Organizations.name.in_(org_names))
            .group_by(
                Organizations.id,
                Organizations.name,
                Buildings.address,
                Buildings.office,
            )
        )

        results = (await self._con.execute(query)).fetchall()

        return [
            {
                "id": result.id,
                "name": result.name,
                "address": result.address,
                "office": result.office,
                "phones": [p for p in result.phones if p is not None],
                "activities": [a for a in result.activities if a is not None],
            }
            for result in results
        ]

    async def build_address_string(self, city: str, street: str, house_num: str) -> str:
        return f"{city}, {street}, {house_num}"

    async def get_organizations_by_address_parts(
        self, city: str, street: str, house_num: str
    ) -> list[str]:
        address_pattern = f"%{city}%{street}%{house_num}%"

        query = (
            select(Organizations.name)
            .join(Buildings)
            .where(Buildings.address.ilike(address_pattern))
        )
        query_res = (await self._con.execute(query)).scalars().all()
        return list(query_res)

    async def get_organizations_by_ancestor_activity_optimized(
        self, ancestor_name: str
    ) -> list[str]:
        query = (
            select(distinct(Organizations.name))
            .join(OrganizationActivities)
            .join(Activities)
            .join(ActivityClosure, ActivityClosure.descendant_id == Activities.id)
            .where(
                ActivityClosure.ancestor_id
                == (select(Activities.id).where(Activities.name == ancestor_name))
            )
        )
        query_res = (await self._con.execute(query)).scalars().all()
        return list(query_res)

    async def get_organization_full_info_by_name(self, org_name: str) -> dict | None:
        query = (
            select(
                Organizations.name,
                Buildings.address,
                Buildings.office,
                func.array_agg(distinct(Phones.phone_number)).label("phones"),
                func.array_agg(distinct(Activities.name)).label("activities"),
            )
            .select_from(Organizations)
            .join(Buildings, isouter=True)
            .join(OrganizationPhones, isouter=True)
            .join(Phones, isouter=True)
            .join(OrganizationActivities, isouter=True)
            .join(Activities, isouter=True)
            .where(Organizations.name == org_name)
            .group_by(Organizations.name, Buildings.address, Buildings.office)
        )

        result = (await self._con.execute(query)).first()
        if not result:
            return None

        return {
            "name": result.name,
            "address": result.address,
            "office": result.office,
            "phones": [p for p in result.phones if p is not None],
            "activities": [a for a in result.activities if a is not None],
        }
