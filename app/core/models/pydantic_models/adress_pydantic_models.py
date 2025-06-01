from pydantic import BaseModel


class Address(BaseModel):
    address: str
    office: int
