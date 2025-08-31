"""This module handles Base Class for all SqlAlchemy Models."""
import re
import uuid
from datetime import UTC, datetime

from sqlalchemy import UUID, DateTime
from sqlalchemy.orm import (DeclarativeBase, Mapped, declared_attr,
                            mapped_column)


class Base(DeclarativeBase):
    """SqlAlchemy Model base class."""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=lambda: datetime.now(UTC)
    )


    @declared_attr
    def __tablename__(cls) -> str:  # pylint: disable=no-self-argument
        """Converts __tablename__ from CamelCase to snake_case according class name."""
        _splitted_words = re.findall("[A-Z][^A-Z]*", cls.__name__)
        _snake_case = "_".join(word.lower() for word in _splitted_words)

        if _snake_case.endswith("y") and _snake_case[-2] not in "aeiou":
            _snake_case = f"{_snake_case[:-1]}ies"
        elif _snake_case.endswith(("s", "ss", "sh", "ch", "x", "z")):
            return f"{_snake_case[:-1]}es"
        else:
            return f"{_snake_case[:]}s"
