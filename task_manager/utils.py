from uuid import UUID
from fastapi import HTTPException, status

from .api import SessionDep
from .crud import get_task


async def get_existing_task(task_id: UUID, session: SessionDep):
    task = await get_task(session, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found"
        )
    return task
