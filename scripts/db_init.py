"""This module adds an ADMIN and ANONYMOUS user to ddbb."""
import asyncio
import os

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.models import User
from src.utils.enumerators import UserType


PG_URL = os.getenv("DATABASE_URL")
async_engine = create_async_engine(url=PG_URL)
async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)


async def init() -> None:
    """Initialice default users if applies."""
    async with async_session() as db:
        stmt_adm = select(User).filter(User.email == "AdminEmail@outlook.com")
        stmt_an = select(User).filter(User.email == "AnEmail@outlook.com")
        result_adm = await db.scalar(stmt_adm)
        result_an = await db.scalar(stmt_an)
        if not result_adm:
            db.add(
                User(
                    email="AdminEmail@outlook.com",
                    password="$2b$12$Js1Z.KmHd9CYOK3iwWP4iOwiiALu8aFsLx7EjFjWEjxgdJdpL.Wd2",
                    user_type=UserType.ADMIN.value
                )
            )
            await db.commit()

        if not result_an:
            db.add(
                User(
                    email="AnEmail@outlook.com",
                    password="$2b$12$rYydkMQROGgV7sIMCEaI1uy/MZGwR4sTYoKOOFd7uYXRBMt9DrdaO",
                    user_type=UserType.ANONYMOUS.value
                )
            )
            await db.commit()

    return


if __name__ == "__main__" and os.getenv("APP_ENVIRONMENT") == "development":
    asyncio.run(init())
