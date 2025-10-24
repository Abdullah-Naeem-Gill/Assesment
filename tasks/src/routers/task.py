from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
from src.core_db.database import get_db
from src.models.task import Task, TaskStatus, TaskPriority
from src.schemas.task import TaskCreate, TaskStatistics, TaskUpdate, TaskResponse

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    request: TaskCreate,
    db: Session = Depends(get_db)
):
    task = Task(**request.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    status: Optional[TaskStatus] = Query(None, description="Filter by status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by priority"),
    db: Session = Depends(get_db)
):
    query = db.query(Task)
    
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    
    tasks = query.all()
    return tasks


@router.get("/statistics", response_model=TaskStatistics)
def get_task_statistics(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    
    total_tasks = len(tasks)
    by_status = {status.value: 0 for status in TaskStatus}
    by_priority = {priority.value: 0 for priority in TaskPriority}
    
    for task in tasks:
        by_status[task.status.value] += 1
        by_priority[task.priority.value] += 1
    
    completed_percentage = (
        round(by_status["completed"] / total_tasks * 100, 2) 
        if total_tasks > 0 else 0.0
    )
    
    return TaskStatistics(
        total_tasks=total_tasks,
        by_status=by_status,
        by_priority=by_priority,
        completed_percentage=completed_percentage
    )


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    request: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    update_data = request.model_dump(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        
        for key, value in update_data.items():
            setattr(task, key, value)
        
        db.commit()
        db.refresh(task)
    
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    db.delete(task)
    db.commit()
    
    return None