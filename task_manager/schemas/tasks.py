from __future__ import annotations
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field
from task_manager.db.models.task import TaskStatus


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=10_000)


class TaskCreate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=10_000)
    status: Optional[TaskStatus] = None


class TaskUpdate(BaseModel):
    title: str = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=10_000)
    status: Optional[TaskStatus] = None


class TaskOut(TaskBase):
    id: UUID

    class Config:
        from_attributes = True
