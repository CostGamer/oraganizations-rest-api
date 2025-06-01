from typing import TYPE_CHECKING

from geoalchemy2 import Geography
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base_sql_model import Base

if TYPE_CHECKING:
    from .organizations_sql_model import Organizations


class Buildings(Base):
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
