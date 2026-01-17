from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from core.database import get_db
from core.deps import get_current_user
from models.user import User
from models.task import Task
from schemas.task import TaskCreate, TaskRead, TaskUpdate
from typing import cast

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskRead)
def create_task(data: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = Task(
        title=data.title,
        description=data.description,
        id_owner=current_user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("", response_model=list[TaskRead])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Список тасков"""
    return (
        db.query(Task)
        .filter(Task.id_owner == cast(int, current_user.id))
        .order_by(Task.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
        task_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """Инфо по task по id"""
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.id_owner == cast(int, current_user.id))
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Меняет task по id"""
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.id_owner == cast(int, current_user.id))
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if data.title is not None:
        task.title = data.title
    if data.description is not None:
        task.description = data.description
    if data.is_done is not None:
        task.is_done = data.is_done

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Удаляет task по id"""
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.id_owner == cast(int, current_user.id))
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"status": "deleted"}
