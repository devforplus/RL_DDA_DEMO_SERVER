from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from ..config import settings


engine: AsyncEngine = create_async_engine(settings.sqlalchemy_dsn, pool_pre_ping=True)
async_session_factory = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


