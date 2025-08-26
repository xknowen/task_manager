from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, status, Depends

from task_manager.schemas.tasks import (
    TaskCreate,
    TaskUpdate,
    TaskOut,
)
from task_manager.services.utils import get_existing_task
from task_manager.db.dependencies import SessionDep
from task_manager.services.task_service import TaskService
from task_manager.services.utils import get_task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskOut)
async def create_task(
    payload: TaskCreate, service: TaskService = Depends(get_task_service)
):
    return await service.create(payload)


@router.get("/{task_id}", response_model=TaskOut)
async def get_task(task_id: UUID, session: SessionDep):
    return await get_existing_task(task_id, session)


@router.get("/", response_model=dict[str, object])
async def list_tasks(
    limit: int = 50,
    offset: int = 0,
    service: TaskService = Depends(get_task_service),
):
    items = await service.list(limit=limit, offset=offset)
    total = len(items)
    return {
        "items": [TaskOut.model_validate(i) for i in items],
        "total": total,
    }


@router.patch("/{task_id}")
async def update_task(
    task_id: UUID,
    payload: TaskUpdate,
    session: SessionDep,
    service: TaskService = Depends(get_task_service),
):
    await get_existing_task(task_id, session)
    return await service.update(task_id, payload)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    session: SessionDep,
    service: TaskService = Depends(get_task_service),
):
    await get_existing_task(task_id, session)
    await service.delete(task_id)
