from __future__ import annotations

from fastapi import APIRouter, Depends, status

from .deps import SessionDep
from .utils import get_existing_task
from .schemas import TaskCreate, TaskRead, TaskUpdate, TaskList, TaskQuery
from .crud import create_task, list_tasks, update_task, delete_task


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task_endpoint(payload: TaskCreate, session: SessionDep):
    task = await create_task(session, payload)
    return task


@router.get("/{task_id}", response_model=TaskRead)
async def get_task_endpoint(task=Depends(get_existing_task)):
    return task


@router.get("/", response_model=TaskList)
async def list_tasks_endpoint(session: SessionDep, params: TaskQuery = Depends()):
    items, total = await list_tasks(session, params)
    return TaskList(
        items=items,
        total=total,
        limit=params.limit,
        offset=params.offset,
    )


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task_endpoint(
    payload: TaskUpdate,
    session: SessionDep,
    task=Depends(get_existing_task),
):
    task = await update_task(session, task, payload)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(session: SessionDep, task=Depends(get_existing_task)):
    await delete_task(session, task)
    return None
