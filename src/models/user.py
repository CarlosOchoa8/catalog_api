from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base
from src.utils.enumerators import UserType


class User(Base):
    """User SQLAlchemy Model."""
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    user_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=UserType.ANONYMOUS.value
    )
