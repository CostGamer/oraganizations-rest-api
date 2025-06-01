from typing import TYPE_CHECKING

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base_sql_model import Base

if TYPE_CHECKING:
    from .organization_phones_sql_model import OrganizationPhones


class Phones(Base):
    phone_number: Mapped[str] = mapped_column(unique=True, nullable=False)

    organization_phones: Mapped[list["OrganizationPhones"]] = relationship(
        "OrganizationPhones",
        back_populates="phones",
        uselist=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Phones(phone_number={self.phone_number})>"
