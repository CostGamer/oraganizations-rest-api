from typing import TYPE_CHECKING

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base_sql_model import Base

if TYPE_CHECKING:
    from .token_sql_model import ApiTokens


class Users(Base):
    login: Mapped[str] = mapped_column(unique=True, nullable=False)

    api_tokens: Mapped[list["ApiTokens"]] = relationship(
        "ApiTokens",
        back_populates="user",
        uselist=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Users(login={self.login})>"
