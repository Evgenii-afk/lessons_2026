from __future__ import annotations

import redis
import redis.asyncio as aioredis

from auth.config import Settings


class RedisCodeRepository:
    def __init__(self, settings: Settings) -> None:
        self.redis = redis.Redis.from_url(
            settings.redis_dsn,
            decode_responses=True
        )

    def set_code(self, account_id: int, code: str, ttl_seconds: int) -> None:
        self.redis.setex(
            f"code:{account_id}",
            ttl_seconds,
            code
        )

    def has_code(self, account_id: int) -> bool:
        return self.redis.exists(f"code:{account_id}") == 1

    def clear(self) -> None:
        self.redis.flushdb()


class AsyncRedisCodeRepository:
    def __init__(self, settings: Settings) -> None:
        self.redis = aioredis.from_url(
            settings.redis_dsn,
            decode_responses=True
        )

    async def set_code(self, account_id: int, code: str, ttl_seconds: int) -> None:
        await self.redis.setex(
            f"code:{account_id}",
            ttl_seconds,
            code
        )

    async def has_code(self, account_id: int) -> bool:
        return await self.redis.exists(f"code:{account_id}") == 1

    async def clear(self) -> None:
        await self.redis.flushdb()