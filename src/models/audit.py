"""This module handle important activities along system."""
from uuid import UUID

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class AuditLog(Base):
    """AuditLog SQLAlchemy Model."""

    # Check if this field would be neccesary after
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    action_performed: Mapped[str] = mapped_column(String(20), nullable=False)
    # Pending extract module's name instead being just str
    affected_module: Mapped[str] = mapped_column(String(100), nullable=False)
    ip_address: Mapped[str] = mapped_column(String(50), nullable=False)
    user_agent: Mapped[str] = mapped_column(String(255), nullable=False)
