from pydantic import BaseModel, ConfigDict


class ApiKey(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    token: str
    limit: int


class Address(BaseModel):
    address: str
    office: int


class Organization(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    phones_numbers: list[str]
    address: Address
    activities: list[str]
