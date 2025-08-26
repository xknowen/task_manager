import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.pool import NullPool

from task_manager.db.base import Base
import task_manager.db.models.task

from dotenv import load_dotenv
import os

load_dotenv()

# Берём URL из .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Это конфиг Alembic
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Настройки логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Запуск миграций в offline-режиме (генерация SQL)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Запуск миграций в async-режиме."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def run_migrations() -> None:
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())


run_migrations()
