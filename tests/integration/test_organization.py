import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_organization_by_name(set_auth_headers: AsyncClient) -> None:
    company_name = {"name": "ООО Рога и Копыта"}

    response = await set_auth_headers.get("/organization/name", params=company_name)

    assert response.status_code == 200, (
        f"Expected status code 200, but got {response.status_code}. "
        f"Response: {response.text}"
    )

    response_json = response.json()

    assert "activities" in response_json, "Response does not contain 'activities'"
    assert "address" in response_json, "Response does not contain 'address'"
    assert (
        "phones_numbers" in response_json
    ), "Response does not contain 'phones_numbers'"
    assert "name" in response_json, "Response does not contain 'name'"
    assert response_json["name"] == company_name["name"], (
        f"Expected organization name to be '{company_name['name']}', "
        f"but got '{response_json['name']}'"
    )


# не универсальный тест, т.к. зависит от данных в базе
@pytest.mark.asyncio
async def test_get_organizations_by_address(set_auth_headers: AsyncClient) -> None:
    org_address = {"city": "Москва", "street": "Ленина", "house_num": "1"}

    response = await set_auth_headers.get("/organization/address", params=org_address)

    assert response.status_code == 200, (
        f"Expected status code 200, but got {response.status_code}. "
        f"Response: {response.text}"
    )

    response_json = response.json()

    assert isinstance(response_json, list), "Response should be a list"

    assert (
        len(response_json) == 3
    ), f"Expected 3 organizations, but got {len(response_json)}."

    for org in response_json:
        assert "name" in org, "Organization should have a 'name' field"
        assert "address" in org, "Organization should have an 'address' field"
        assert (
            "phones_numbers" in org
        ), "Organization should have a 'phones_numbers' field"
        assert "activities" in org, "Organization should have an 'activities' field"
