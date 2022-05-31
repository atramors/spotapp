from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from api import models

from api.settings import settings


async_engine = create_async_engine(
    settings.db_dsn,
    pool_pre_ping=True,
    connect_args={"timeout": settings.db_query_timeout}
)

SessionFactory = sessionmaker(autocommit=False,
                              autoflush=False,
                              bind=async_engine,
                              class_=AsyncSession)


async def get_session() -> AsyncSession:
    """Session factory"""
    # create tables in DB
    async with async_engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

    async with SessionFactory() as session:
        async with session.begin():
            yield session
            await session.commit()
