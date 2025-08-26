from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from fastapi import Depends

from task_manager.core.config import get_settings


settings = get_settings()
engine = create_async_engine(settings.database_url, echo=False, future=True)
async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_db_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db_session)]
