from __future__ import annotations

import uuid
from uuid import UUID
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as sqUUID
from sqlalchemy import String, Enum as SAEnum, Text

from .task_status import TaskStatus
from task_manager.db.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[UUID] = mapped_column(
        sqUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        SAEnum(TaskStatus), nullable=False, default=TaskStatus.CREATED
    )
