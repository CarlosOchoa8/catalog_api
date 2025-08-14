"""Generate an Object of CRUD for users. """
from typing import Any, Dict

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base_crud import CRUDBase
from src.models import User
from src.schemas import UserCreateSchema
from src.services.auth import get_password_hash


class CRUDUser(CRUDBase):
    """User CRUD class.
    :param CRUDBase: base CRUD."""

    async def create(self, obj_in: UserCreateSchema | Dict[str, Any], db: AsyncSession) -> User:
        """Create a User object"""
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['password'] = get_password_hash(obj_in_data['password'])
        db_obj = self.model(**obj_in_data)  # type: ignore

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

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
