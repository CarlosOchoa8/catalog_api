"""This module handle db async connection."""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import async_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Database session manager as context."""
    async with async_session() as db:
        try:
            yield db

        except Exception as exc:
            await db.rollback()
            # await db.close()
            raise exc
        # finally:
        #     await db.close()
