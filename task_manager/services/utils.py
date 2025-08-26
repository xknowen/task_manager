from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select

from task_manager.db.models.task import Task
from task_manager.db.dependencies import SessionDep


async def get_existing_task(task_id: UUID, session: SessionDep) -> Task:
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
