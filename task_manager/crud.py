from __future__ import annotations
from uuid import UUID

from sqlalchemy import select, func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Task, TaskStatus
from .schemas import TaskCreate, TaskQuery, TaskUpdate


async def create_task(session: AsyncSession, data: TaskCreate) -> Task:
    task = Task(
        title=data.title, description=data.description, status=TaskStatus.CREATED
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


async def get_task(session: AsyncSession, task_id: UUID | str) -> Task:
    stmt = select(Task).where(Task.id == str(task_id))
    res = await session.execute(stmt)

    return res.scalar_one_or_none()


async def list_tasks(
    session: AsyncSession, params: TaskQuery
) -> tuple[list[Task], int]:
    stmt = select(Task)

    if params.status:
        stmt = stmt.where(Task.status == params.status)

    if params.q:
        like = f"%{params.q}%"
        stmt = stmt.where((Task.title.ilike(like)) | (Task.description.ilike(like)))

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await session.execute(count_stmt)).scalar_one()

    sort_map = {
        "created": Task.id,
        "title": Task.title,
        "status": Task.status,
    }
    order_by_col = sort_map.get(params.sort_by, Task.id)
    order_by = asc(order_by_col) if params.order == "asc" else desc(order_by_col)

    stmt = stmt.order_by(order_by).offset(params.offset).limit(params.limit)

    rows = (await session.execute(stmt)).scalars().all()

    return rows, total


async def update_task(session: AsyncSession, task: Task, data: TaskUpdate) -> Task:
    if data.title is not None:
        task.title = data.title
    if data.description is not None:
        task.description = data.description
    if data.status is not None:
        task.status = data.status

    await session.commit()
    await session.refresh(task)

    return task


async def delete_task(session: AsyncSession, task: Task) -> None:
    await session.delete(task)
    await session.commit()
