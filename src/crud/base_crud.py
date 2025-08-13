import uuid
from typing import Any, Optional, Union, Dict

from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete as sql_delete
from sqlalchemy import select
from sqlalchemy import update as sql_update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import Product, User


class CRUDBase:
    """Base Crud Class."""
    def __init__(self, model):
        """CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        :param model: A SQLAlchemy model class."""
        self.model = model

    async def create(self, db: AsyncSession, obj_in: Dict[str, Any] | dict[str, Any]):
        """Create a ModelType object"""
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self, db: AsyncSession, id: uuid.UUID):
        """Get object by ID"""
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_multi(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        """Get multiple objects"""
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def update(self, db: AsyncSession, db_obj: Union[User, Product], obj_in: dict):
        """Update object"""
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id: uuid.UUID):
        """Delete object by ID"""
        await db.execute(sql_delete(self.model).where(self.model.id == id))
        await db.commit()
        return True
