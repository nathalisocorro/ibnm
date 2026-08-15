from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Logical Tasks"]
)

class LogicalTask(BaseModel):
    task_id: str
    policy_id: str
    intent_id: str
    task_description: str
    status: Literal[
        "GENERATING",
        "VALIDATED",
        "INVALID",
        "CANCELLED",
    ]
    
tasks = [
    {
        "task_id": "task-001",
        "policy_id": "policy-004",
        "intent_id": "1",
        "task_description": "Task #1",
        "status": "GENERATING",
    },
    {
        "task_id": "task-002",
        "policy_id": "policy-004",
        "intent_id": "1",
        "task_description": "Task #2",
        "status": "GENERATING",
    },
]
    
    
@router.get("")
async def get_tasks():
    return {
        "tasks": tasks
    }
    
@router.get("/{task_id}")
async def get_task_by_id(task_id: str):
    found_task = None
    for task in tasks:
        if(task.get("task_id") == task_id):
            found_task = task
    if found_task:
        return {
            "message": "Found task",
            "task": found_task
        }
    else:
        raise HTTPException(
        status_code=404,
        detail="Task not found",
    )
        
@router.get("/status/{status}")
async def get_tasks_by_status(status: str):
    if status == None:
        raise HTTPException(
        status_code=404,
        detail="Route not found",
    )
    found_tasks = []
    for task in tasks:
        if(task.get("status").lower() == status.lower()):
            found_tasks.append(task)
    return {
        "message": "Success" if len(found_tasks) else "Not found",
        "tasks": found_tasks
    }
    
@router.post("")
async def create_task(task: LogicalTask):
    if task:
        tasks.append(task)
        return {
            "message": "Task created successfuly!",
            "task": task
        }
    else:
        return {
            "message": "Error in receiving task",
            "task": None
        }