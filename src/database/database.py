import os
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


PG_PORT = os.getenv("POSTGRES_PORT")
PG_HOST = os.getenv("POSTGRES_HOST")
PG_USER = os.getenv("POSTGRES_USER")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD")
PG_NAME = os.getenv("POSTGRES_NAME")

PG_URL = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_NAME}"

async_engine = create_async_engine(url=PG_URL)

async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)
