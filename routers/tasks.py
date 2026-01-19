from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import cast

from models.user import User
from models.task import Task
from schemas.task import TaskCreate, TaskRead, TaskUpdate
from core.database import get_db
from core.deps import get_current_user
from core.cache import (
    tasks_cache_key,
    cache_get_json,
    cache_set_json,
    invalidate_tasks_cache,
)

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

    invalidate_tasks_cache(current_user.id)

    return task


@router.get("", response_model=list[TaskRead])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Список tasks (с Redis кешем)"""
    user_id = current_user.id
    key = tasks_cache_key(user_id, limit, offset)

    cached = cache_get_json(key)

    if cached is not None:
        print("CACHE HIT", key)
        return cached

    print("CACHE MISS", key)
    tasks = (
        db.query(Task)
        .filter(Task.id_owner == cast(int, current_user.id))
        .order_by(Task.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    payload = [TaskRead.model_validate(t).model_dump() for t in tasks]
    cache_set_json(key, payload)

    return payload


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
        task_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """Инфо task по task_id"""
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
    """Меняет task по task_id"""
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

    invalidate_tasks_cache(current_user.id)

    return task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Удаляет task по task_id"""
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.id_owner == cast(int, current_user.id))
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    invalidate_tasks_cache(current_user.id)

    return {"status": "deleted"}
