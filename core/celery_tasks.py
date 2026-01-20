from core.celery_app import celery
from core.config import logger
import time


@celery.task(name="log_action")
def log_action(text: str) -> None:
    logger.info(text)
    # для тестов и проверки работы Celery
    # logger.info("start")
    # time.sleep(10)
    # logger.info("stop")
