import json
from typing import Any

from core.redis_client import redis_client

CACHE_TTL_SECONDS = 30


def tasks_cache_key(user_id: int, limit: int, offset: int) -> str:
    return f"tasks:{user_id}:limit={limit}:offset={offset}"


def cache_get_json(key: str) -> Any | None:
    raw = redis_client.get(key)
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def cache_set_json(key: str, value: Any, ttl_seconds: int = CACHE_TTL_SECONDS) -> None:
    redis_client.set(key, json.dumps(value, ensure_ascii=False), ex=ttl_seconds)


def invalidate_tasks_cache(user_id: int) -> None:
    pattern = f"tasks:{user_id}:*"
    keys = list(redis_client.scan_iter(match=pattern, count=200))
    if keys:
        redis_client.delete(*keys)
