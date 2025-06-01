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
    from .activities_sql_model import Activities
    from .organizations_sql_model import Organizations


class OrganizationActivities(Base):
    activity_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("activities.id"), nullable=False
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id"), nullable=False
    )

    activities: Mapped["Activities"] = relationship(
        "Activities",
        back_populates="organization_activities",
    )
    organizations: Mapped["Organizations"] = relationship(
        "Organizations",
        back_populates="organization_activities",
    )
