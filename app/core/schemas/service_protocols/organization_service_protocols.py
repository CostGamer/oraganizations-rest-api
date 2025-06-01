from typing import Protocol

from pydantic import UUID4

from app.core.models.pydantic_models import Organization


class GetOrganizationByNameServiceProtocol(Protocol):
    async def __call__(self, name: str) -> Organization:
        pass


class GetOrganizationsFromAddressServiceProtocol(Protocol):
    async def __call__(
        self, city: str, street: str, house_num: str
    ) -> list[Organization]:
        pass


class GetOrganizationsFromActivityServiceProtocol(Protocol):
    async def __call__(self, activity: str) -> list[Organization]:
        pass


class GetOrganizationByIDServiceProtocol(Protocol):
    async def __call__(self, org_id: UUID4) -> Organization:
        pass


class GetOrganizationsFromAncestorActivityServiceProtocol(Protocol):
    async def __call__(self, activity: str) -> list[Organization]:
        pass


class GetOrganizationsFromGeoServiceProtocol(Protocol):
    async def __call__(
        self, latitude: float, longitude: float, radius: float
    ) -> list[Organization]:
        pass
