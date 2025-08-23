from __future__ import annotations
from typing import Optional, Literal
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from .models import TaskStatus


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


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: Optional[str]
    status: TaskStatus


class TaskList(BaseModel):
    items: list[TaskRead]
    total: int
    limit: int
    offset: int


class TaskQuery(BaseModel):
    status: Optional[TaskStatus] = None
    q: Optional[str] = Field(default=None, description="Поиск по названию/описанию")
    limit: int = Field(default=50, ge=1, le=200)
    offset: int = Field(default=0, ge=0)
    sort_by: Literal["created", "title", "status"] = "created"
    order: Literal["asc", "desc"] = "asc"
