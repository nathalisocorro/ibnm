from typing import Any
from uuid import UUID

from pydantic import BaseModel


class PolicyProposedEvent(BaseModel):
    event_type: str
    event_id: UUID
    timestamp: str
    policy_id: UUID
    intent_id: UUID
    payload: dict[str, Any]