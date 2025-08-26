from typing import Annotated

from fastapi import Depends

from task_manager.db.dependencies import SessionDep
from task_manager.repositories.task_repository import TaskRepository


async def get_task_repository(session: SessionDep) -> TaskRepository:
    return TaskRepository(session)


RepositoryDep = Annotated[TaskRepository, Depends(get_task_repository)]
