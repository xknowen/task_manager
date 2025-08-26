from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from task_manager.repositories.task_repository import TaskRepository
from task_manager.schemas.tasks import TaskCreate, TaskUpdate, TaskOut


class TaskService:
    def __init__(self, session: AsyncSession):
        self.repo = TaskRepository(session)

    async def create(self, payload: TaskCreate) -> TaskOut:
        task = await self.repo.create(payload.model_dump())
        return TaskOut.model_validate(task, from_attributes=True)

    async def get(self, task_id: UUID):
        return await self.repo.get(task_id)

    async def list(self, limit: int, offset: int):
        return await self.repo.list(limit, offset)

    async def update(self, task_id: UUID, payload: TaskUpdate) -> TaskOut:
        task = await self.repo.update(task_id, payload.model_dump(exclude_unset=True))
        return TaskOut.model_validate(task, from_attributes=True)

    async def delete(self, task_id: UUID) -> bool:
        return await self.repo.delete(task_id)
