from celery import Celery
from core.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery = Celery(
    "todo_manager",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["core.celery_tasks"],
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
