import json
from typing import Any, Optional

import redis

from app.core.settings import settings


class CacheService:
    def __init__(self) -> None:
        self.client = None
        if settings.enable_redis_cache:
            try:
                self.client = redis.Redis.from_url(settings.redis_url, decode_responses=True)
                self.client.ping()
            except Exception:
                self.client = None

    def get_json(self, key: str) -> Optional[dict[str, Any]]:
        if not self.client:
            return None
        value = self.client.get(key)
        return json.loads(value) if value else None

    def set_json(self, key: str, value: dict[str, Any], ttl: int) -> None:
        if not self.client:
            return
        self.client.setex(key, ttl, json.dumps(value))
