from sqlalchemy.orm import Session
from app.db.models import LogicalTask as LogicalTaskModel
from app.schemas.logical_task import LogicalTaskCreate


def create_logical_task(
    db: Session,
    policy_id,
    intent_id,
    task_description: str = "",
):
    new_task = LogicalTaskModel(
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