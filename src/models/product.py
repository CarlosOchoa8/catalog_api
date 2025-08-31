from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base


class Product(Base):
    """Product SQLAlchemy Model."""

    sku: Mapped[str] = mapped_column(
        String(255), unique=True,
        nullable=False, index=True,
    )
    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )
    price: Mapped[float] = mapped_column(
        Float(12, 4),
        nullable=False,
    )
    brand: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
