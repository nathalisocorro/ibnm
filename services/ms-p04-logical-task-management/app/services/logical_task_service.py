from sqlalchemy.orm import Session

from app.db.models import LogicalTask
from app.schemas.events import PolicyProposedEvent


def create_logical_task(
    db: Session,
    policy_id,
    intent_id,
    task_description: str = "",
):
    new_task = LogicalTask(
        policy_id=policy_id,
        intent_id=intent_id,
        task_description=task_description,
        status="GENERATING",
        try_number=1,
        version=1,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def process_policy_proposed(
    db: Session,
    event: PolicyProposedEvent,
):
    task_description = event.payload.get(
        "task_description",
        "",
    )

    return create_logical_task(
        db=db,
        policy_id=event.policy_id,
        intent_id=event.intent_id,
        task_description=task_description,
    )