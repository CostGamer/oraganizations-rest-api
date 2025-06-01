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
    from .organization_activities_sql_model import OrganizationActivities


class Activities(Base):
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    organization_activities: Mapped[list["OrganizationActivities"]] = relationship(
        "OrganizationActivities",
        back_populates="activities",
        uselist=True,
        cascade="all, delete-orphan",
    )
    descendants: Mapped[list["ActivityClosure"]] = relationship(
        "ActivityClosure",
        back_populates="descendant",
        foreign_keys="[ActivityClosure.ancestor_id]",
        uselist=True,
        cascade="all, delete-orphan",
    )
    ancestors: Mapped[list["ActivityClosure"]] = relationship(
        "ActivityClosure",
        back_populates="ancestor",
        foreign_keys="[ActivityClosure.descendant_id]",
        uselist=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Activities(name={self.name})>"


class ActivityClosure(Base):
    ancestor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("activities.id"), nullable=False
    )
    descendant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("activities.id"), nullable=False
    )

    ancestor: Mapped["Activities"] = relationship(
        "Activities",
        back_populates="descendants",
        foreign_keys=[ancestor_id],
    )
    descendant: Mapped["Activities"] = relationship(
        "Activities",
        back_populates="ancestors",
        foreign_keys=[descendant_id],
    )
