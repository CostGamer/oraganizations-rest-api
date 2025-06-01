import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base_sql_model import Base

if TYPE_CHECKING:
    from .organizations_sql_model import Organizations
    from .phones_sql_model import Phones


class OrganizationPhones(Base):
    phone_number_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("phones.id"), nullable=False
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id"), nullable=False
    )

    phones: Mapped["Phones"] = relationship(
        "Phones",
        back_populates="organization_phones",
    )
    organizations: Mapped["Organizations"] = relationship(
        "Organizations",
        back_populates="organization_phones",
    )
