"""Generate an Object of CRUD for users. """
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.crud.base_crud import CRUDBase
from src.models import User
from sqlalchemy.exc import IntegrityError

class CRUDUser(CRUDBase):
    """User CRUD class.
    :param CRUDBase: base CRUD."""

    async def get_by_email(self, email: str, db: AsyncSession) -> User:
        """Retrieve user by email.
        :param email: user's email.
        :param db: Async db session.
        :return: User obj."""
        try:
            stmt = select(self.model).filter(self.model.email == email)
            return await db.scalar(stmt)

        except IntegrityError as ie:
            await db.rollback()
            raise ie



user_crud = CRUDUser(User)
