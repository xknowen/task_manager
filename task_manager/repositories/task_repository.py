from __future__ import annotations

from typing import List
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from task_manager.db.models.task import Task
from task_manager.services.utils import get_existing_task


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: dict) -> Task:
        task = Task(**data)
        self.session.add(task)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def get(self, task_id: UUID) -> Task | None:
        res = await self.session.execute(select(Task).where(Task.id == task_id))

        return res.scalar_one_or_none()

    async def list(self, limit: int = 50, offset: int = 0) -> List[Task]:
        res = await self.session.execute(select(Task).limit(limit).offset(offset))
        return list(res.scalars())

    async def update(self, task_id: UUID, data: dict) -> Task:
        task = await get_existing_task(task_id, self.session)
        for k, v in data.items():
            setattr(task, k, v)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete(self, task_id: UUID) -> bool:
        res = await self.session.execute(
            delete(Task).where(Task.id == task_id).returning(Task.id)
        )
        return res.scalar_one_or_none() is not None
