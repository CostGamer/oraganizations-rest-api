from pydantic import UUID4

from app.core.custom_exceptions import (
    ActivityNotFoundError,
    AddressNotFoundError,
    OrganizationNotFoundError,
)
from app.core.pydantic_schemas import Organization
from app.repositories.organization_repo import OrganizationRepo


class OrganizationCommonService:
    """Common service for interacting with organization data.

    This service provides methods for retrieving detailed information about organizations
    from the repository. It allows fetching an organization by its name and offers reusable
    logic for other services related to organizations.

    Args:
        organization_repo (OrganizationRepo): Repository for organization-related data.

    Methods:
        get_organization_by_name(name: str) -> Organization:
            Fetches detailed information about an organization based on its name.
    """

    def __init__(
        self,
        organization_repo: OrganizationRepo,
    ) -> None:
        self._organization_repo = organization_repo

    async def get_organization_by_name(self, name: str) -> Organization:
        """Fetches detailed information about an organization by its name.

        Args:
            name (str): The name of the organization to retrieve.

        Returns:
            Organization: An object containing the organization's details, including
            name, phone numbers, address, and activities.

        Raises:
            OrganizationNotFoundError: If no organization is found with the given name.
        """
        org_id = await self._organization_repo.get_organization_id_by_name(name)
        if org_id is None:
            raise OrganizationNotFoundError

        organizations_phones = await self._organization_repo.get_organization_phones(
            org_id
        )
        organizations_activities = (
            await self._organization_repo.get_organization_activities(org_id)
        )
        organization_address = await self._organization_repo.get_organization_address(
            org_id
        )

        return Organization(
            name=name,
            phones_numbers=organizations_phones,
            address=organization_address,
            activities=organizations_activities,
        )


class GetOrganizationByNameService(OrganizationCommonService):
    """Service for retrieving detailed information about an organization by name.

    This service extends the `OrganizationCommonService` and provides the functionality
    to fetch an organization's details (ID, phone numbers, activities, and address)
    based on its name. If the organization is not found, an exception is raised.

    Args:
        organization_repo (OrganizationRepo): Repository for organization-related data.

    Methods:
        __call__(name: str) -> Organization:
            Retrieves detailed information about the organization with the given name.
    """

    def __init__(
        self,
        organization_repo: OrganizationRepo,
    ) -> None:
        super().__init__(organization_repo)

    async def __call__(self, name: str) -> Organization:
        return await self.get_organization_by_name(name)


class GetOrganizationsFromAddressService(OrganizationCommonService):
    """Service for retrieving organizations based on a given address.

    This service fetches all organizations located at a specific address
    (city, street, and house number). If the address does not exist, an exception is raised.

    Args:
        organization_repo (OrganizationRepo): Repository for organization-related data.

    Methods:
        __call__(city: str, street: str, house_num: str) -> list[Organization]:
            Retrieves all organizations located at the specified address.

        _compose_address(city: str, street: str, house_num: str) -> str:
            Helper method to compose a full address string from the provided city, street, and house number.
    """

    def __init__(
        self,
        organization_repo: OrganizationRepo,
    ) -> None:
        super().__init__(organization_repo)

    async def __call__(
        self, city: str, street: str, house_num: str
    ) -> list[Organization]:
        address = self._compose_adress(city, street, house_num)
        if not await self._organization_repo.check_adress_exists(address):
            raise AddressNotFoundError

        organization_list = (
            await self._organization_repo.get_all_organizations_from_address(address)
        )
        final_organization_list = [
            await self.get_organization_by_name(organization_name)
            for organization_name in organization_list
        ]

        return final_organization_list

    def _compose_adress(self, city: str, street: str, house_num: str) -> str:
        """Composes a full address string from city, street, and house number.

        Args:
            city (str): The city where the organization is located.
            street (str): The street name.
            house_num (str): The house number.

        Returns:
            str: The full address string.
        """
        return f"г. {city}, ул. {street} {house_num}"


class GetOrganizationsFromActivityService(OrganizationCommonService):
    """Service for retrieving organizations based on a specific activity.

    This service fetches all organizations involved in a specific activity.
    If the activity does not exist, an exception is raised.

    Args:
        organization_repo (OrganizationRepo): Repository for organization-related data.

    Methods:
        __call__(activity: str) -> list[Organization]:
            Retrieves all organizations associated with the specified activity.
    """

    def __init__(
        self,
        organization_repo: OrganizationRepo,
    ) -> None:
        super().__init__(organization_repo)

    async def __call__(self, activity: str) -> list[Organization]:
        check_activity_exists = await self._organization_repo.check_activity_exists(
            activity
        )
        if not check_activity_exists:
            raise ActivityNotFoundError

        organization_list = (
            await self._organization_repo.get_all_organizations_from_activity(activity)
        )
        final_organization_list = [
            await self.get_organization_by_name(organization_name)
            for organization_name in organization_list
        ]

        return final_organization_list


class GetOrganizationByIDService:
    """Service for retrieving detailed information about an organization by its ID.

    This service fetches the organization's name, phone numbers, activities,
    and address based on the provided organization ID. If the organization is not found,
    an exception is raised.

    Args:
        organization_repo (OrganizationRepo): Repository for organization-related data.

    Methods:
        __call__(org_id: UUID4) -> Organization:
            Retrieves detailed information about the organization with the given ID.
    """

    def __init__(
        self,
        organization_repo: OrganizationRepo,
    ) -> None:
        self._organization_repo = organization_repo

    async def __call__(self, org_id: UUID4) -> Organization:
        """Fetches detailed information about an organization by its ID.

        Args:
            org_id (UUID4): The ID of the organization to retrieve.

        Returns:
            Organization: An object containing the organization's details, including
            name, phone numbers, address, and activities.

        Raises:
            OrganizationNotFoundError: If no organization is found with the given ID.
        """
        get_organization_name = await self._organization_repo.get_organization_by_id(
            org_id
        )
        if not get_organization_name:
            raise OrganizationNotFoundError

        organizations_phones = await self._organization_repo.get_organization_phones(
            org_id
        )
        organizations_activities = (
            await self._organization_repo.get_organization_activities(org_id)
        )
        organization_address = await self._organization_repo.get_organization_address(
            org_id
        )

        return Organization(
            name=get_organization_name,
            phones_numbers=organizations_phones,
            address=organization_address,
            activities=organizations_activities,
        )


class GetOrganizationsFromAncestorActivityService(OrganizationCommonService):
    """Service for retrieving organizations associated with a given ancestor activity.

    This service checks if an activity exists and fetches a list of organizations
    linked to that activity and its ancestors. If no such activity is found, an exception
    is raised.

    Args:
        organization_repo (OrganizationRepo): Repository for organization-related data.

    Methods:
        __call__(activity: str) -> list[Organization]:
            Retrieves a list of organizations linked to the ancestor activity.
    """

    def __init__(
        self,
        organization_repo: OrganizationRepo,
    ) -> None:
        super().__init__(organization_repo)

    async def __call__(self, activity: str) -> list[Organization]:
        """Retrieves organizations linked to the ancestor activity.

        Args:
            activity (str): The ancestor activity to search for associated organizations.

        Returns:
            list[Organization]: A list of organizations associated with the activity and its ancestors.

        Raises:
            ActivityNotFoundError: If the specified activity is not found in the system.
        """
        check_activity_exists = await self._organization_repo.check_activity_exists(
            activity
        )
        if not check_activity_exists:
            raise ActivityNotFoundError

        activities_list = (
            await self._organization_repo.get_all_activities_from_ancestor(activity)
        )

        organization_names = set()
        for activity in activities_list:
            organizations_from_activity = (
                await self._organization_repo.get_all_organizations_from_activity(
                    activity
                )
            )
            organization_names.update(organizations_from_activity)

        final_organization_list = []
        for organization_name in organization_names:
            organization_info = await self.get_organization_by_name(organization_name)
            final_organization_list.append(organization_info)

        return final_organization_list


class GetOrganizationsFromGeoService(OrganizationCommonService):
    """Service for retrieving organizations located within a specified geographic radius.

    This service retrieves organizations based on their proximity to a given latitude and
    longitude, considering a specified radius. If no organizations are found within the radius,
    an empty list is returned.

    Args:
        organization_repo (OrganizationRepo): Repository for organization-related data.

    Methods:
        __call__(latitude: float, longitude: float, radius: float) -> list[Organization]:
            Retrieves a list of organizations within the specified geographic radius.
    """

    def __init__(
        self,
        organization_repo: OrganizationRepo,
    ) -> None:
        super().__init__(organization_repo)

    async def __call__(
        self, latitude: float, longitude: float, radius: float
    ) -> list[Organization]:
        """Retrieves organizations within a given geographic radius.

        Args:
            latitude (float): The latitude of the center point.
            longitude (float): The longitude of the center point.
            radius (float): The radius (in kilometers) within which to search for organizations.

        Returns:
            list[Organization]: A list of organizations within the specified radius.

        """
        organizations_list = (
            await self._organization_repo.get_organizations_within_radius(
                latitude, longitude, radius
            )
        )

        final_organization_list = []
        for organization_name in organizations_list:
            organization_info = await self.get_organization_by_name(organization_name)
            final_organization_list.append(organization_info)

        return final_organization_list
