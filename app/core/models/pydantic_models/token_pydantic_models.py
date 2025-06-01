from pydantic import BaseModel, ConfigDict


class ApiKey(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    token: str
    limit: int
