import os
import sys

sys.path.append(os.path.join(os.getcwd(), ".."))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


async_engine = create_async_engine(
    f"sqlite+aiosqlite:///{'db.sqlite'}",
    echo=True,
)

async_session_maker = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def create_tables():
    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session():
    async with async_session_maker() as session:
        yield session
