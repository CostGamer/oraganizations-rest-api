import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base_sql_model import Base

if TYPE_CHECKING:
    from .users_sql_model import Users


class ApiTokens(Base):
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
