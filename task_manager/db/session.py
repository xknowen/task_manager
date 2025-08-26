from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from task_manager.core.config import get_settings


settings = get_settings()
engine = create_async_engine(settings.database_url, echo=False, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
