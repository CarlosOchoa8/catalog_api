"""
Generate an Object of CRUD for products
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base_crud import CRUDBase
from src.models import Product


class CRUDProduct(CRUDBase):
    """Product CRUD class.
    :param CRUDBase: base CRUD."""

    async def get_by_sku(self, sku: str, db: AsyncSession):
        """Get product by SKU.
        :param sku: Product SKU to search for.
        :param db: Async database session.
        :return: Product object if found, None otherwise."""
        stmt = select(self.model).where(self.model.sku == sku)
        return await db.scalar(stmt)

    async def get_by_name(self, name: str, db: AsyncSession):
        """Retrieve product by its name.
        :param name: Product name to search for.
        :param db: Async database session.
        :return: Product object if found, None otherwise."""
        stmt = select(self.model).where(self.model.name == name)
        return await db.scalar(stmt)


product_crud = CRUDProduct(Product)
