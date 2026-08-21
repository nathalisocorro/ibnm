from typing import Optional, Any
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

class LogicalTaskCreate(BaseModel):
    policy_id: UUID
    intent_id: UUID
    task_description: str = ""
    status: str = "GENERATING"

class LogicalTaskResponse(BaseModel):
    task_id: UUID
    policy_id: UUID
    intent_id: UUID
    task_description: str

    task_json: Optional[dict[str, Any]] = None
    parameters_to_monitor: Optional[list[str]] = None
    generated_by: Optional[str] = None
    generated_at: Optional[datetime] = None

    status: str
    try_number: int
    version: int

