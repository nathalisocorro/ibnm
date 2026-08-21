from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import LogicalTask as LogicalTaskModel
from fastapi import Query

from uuid import UUID

from app.schemas.logical_task import LogicalTaskCreate, LogicalTaskResponse
from app.services.logical_task_service import create_logical_task

router = APIRouter(
    prefix="/api/v1/logical-task-management",
    tags=["Logical Tasks"]
)


@router.get("/health")
async def health(db: Session = Depends(get_db)):
    if(db):
        return {
                "status": "ok",
                "service": "ms-p04-logical-task-management",
            }
    else:
        return {
                "status": "fault",
                "service": "ms-p04-logical-task-management",
            } 
 
@router.get("/tasks")
async def get_tasks(
    db: Session = Depends(get_db),
    intent_id: Annotated[Optional[str], Query()] = None,
    status: Annotated[Optional[str], Query()] = None,
    policy_id: Annotated[Optional[str], Query()] = None
):
    db_tasks = db.query(LogicalTaskModel)

    if intent_id:
        db_tasks = db_tasks.filter(LogicalTaskModel.intent_id == intent_id)
    if status:
        db_tasks = db_tasks.filter(LogicalTaskModel.status.ilike(f"%{status}%"))
    if policy_id:
        db_tasks = db_tasks.filter(LogicalTaskModel.policy_id == policy_id)

    db_tasks = db_tasks.all()

    return {
        "message": "Success",
        "tasks": [
            {
                "task_id": task.task_id,
                "policy_id": task.policy_id,
                "intent_id": task.intent_id,
                "task_description": task.task_description,
                "status": task.status,
                "parameters_to_monitor": task.parameters_to_monitor,
                "task_json": task.task_json,
                "try_number": task.try_number,
                "version": task.version
            }
            for task in db_tasks
        ],
    }
    
@router.get("/tasks/{task_id}")
async def get_task_by_id(
    task_id: UUID,
    db: Session = Depends(get_db),
):
    db_task = db.query(LogicalTaskModel).filter(LogicalTaskModel.task_id == task_id).first()

    if not db_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return {
        "message": "Success",
        "task": {
            "task_id": db_task.task_id,
            "policy_id": db_task.policy_id,
            "intent_id": db_task.intent_id,
            "task_description": db_task.task_description,
            "status": db_task.status,
        }
    }

@router.post("")
async def create_task(
    task: LogicalTaskCreate,
    db: Session = Depends(get_db),
):
    new_task = create_logical_task(
        db=db,
        policy_id=task.policy_id,
        intent_id=task.intent_id,
        task_description=task.task_description
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "message": "Task created successfully!",
        "task": {
            "task_id": new_task.task_id,
            "policy_id": new_task.policy_id,
            "intent_id": new_task.intent_id,
            "task_description": new_task.task_description,
            "status": new_task.status,
            "try_number": new_task.try_number,
            "version": new_task.version,
        },
    }