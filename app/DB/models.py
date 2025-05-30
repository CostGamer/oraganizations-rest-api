import uuid
from datetime import datetime

from geoalchemy2 import Geography
from sqlalchemy import ForeignKey, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )


class Organizations(Base):
    __tablename__ = "organizations"

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


class Buildings(Base):
    __tablename__ = "buildings"

    address: Mapped[str] = mapped_column(nullable=False)
    office: Mapped[int] = mapped_column(nullable=False)
    location: Mapped[Geography] = mapped_column(
        Geography(geometry_type="POINT", srid=4326), nullable=False
    )

    organization: Mapped["Organizations"] = relationship(
        "Organizations",
        back_populates="building",
    )

    def __repr__(self) -> str:
        return f"<Buildings(address={self.address}, office={self.office}, location={self.location})>"


class Phones(Base):
    __tablename__ = "phones"

    phone_number: Mapped[str] = mapped_column(unique=True, nullable=False)

    organization_phones: Mapped[list["OrganizationPhones"]] = relationship(
        "OrganizationPhones",
        back_populates="phones",
        uselist=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Phones(phone_number={self.phone_number})>"


class OrganizationPhones(Base):
    __tablename__ = "organization_phones"

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


class Activities(Base):
    __tablename__ = "activities"

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
    __tablename__ = "activity_closure"

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


class OrganizationActivities(Base):
    __tablename__ = "organization_activities"

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


class Users(Base):
    __tablename__ = "users"

    login: Mapped[str] = mapped_column(unique=True, nullable=False)

    api_tokens: Mapped[list["ApiTokens"]] = relationship(
        "ApiTokens",
        back_populates="user",
        uselist=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Users(login={self.login})>"


class ApiTokens(Base):
    __tablename__ = "api_tokens"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    token: Mapped[str] = mapped_column(unique=True, nullable=False)
    limit: Mapped[int] = mapped_column(default=100, nullable=False)
    last_update: Mapped[datetime] = mapped_column(default=func.now())

    user: Mapped["Users"] = relationship(
        "Users",
        back_populates="api_tokens",
    )

    def __repr__(self) -> str:
        return f"<ApiTokens(token={self.token}, limit={self.limit}, last_update={self.last_update})>"
