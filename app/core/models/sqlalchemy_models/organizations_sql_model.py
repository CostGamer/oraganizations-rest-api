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
    from .buildings_sql_model import Buildings
    from .organization_activities_sql_model import OrganizationActivities
    from .organization_phones_sql_model import OrganizationPhones


class Organizations(Base):
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    building_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("buildings.id"), nullable=False
    )

    organization_phones: Mapped[list["OrganizationPhones"]] = relationship(
        "OrganizationPhones",
        back_populates="organizations",
        uselist=True,
        cascade="all, delete-orphan",
    )
    building: Mapped["Buildings"] = relationship(
        "Buildings",
        back_populates="organization",
    )
    organization_activities: Mapped[list["OrganizationActivities"]] = relationship(
        "OrganizationActivities",
        back_populates="organizations",
        uselist=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Organization(name={self.name})>"
