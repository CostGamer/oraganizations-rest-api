from pydantic import BaseModel, ConfigDict

from .adress_pydantic_models import Address


class Organization(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    phones_numbers: list[str]
    address: Address
    activities: list[str]
