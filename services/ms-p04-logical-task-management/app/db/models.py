import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class LogicalTask(Base):
    __tablename__ = "logical_tasks"

    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    policy_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    intent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    task_description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    task_json: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    parameters_to_monitor: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    generated_by: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    generated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    try_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )
    
    
class LogicalTaskRegistry(Base):
    __tablename__ = "logical_task_registry"

    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )

    policy_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    intent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )

    task_json: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    parameters_to_monitor: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    generated_by: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    generated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )