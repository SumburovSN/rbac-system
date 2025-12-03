import time
from app.infrastructure.redis_client import redis_client


class TokenBlacklistService:
    KEY_PREFIX = "blacklist:"

    def add(self, token: str, expires_at: int):
        ttl = expires_at - int(time.time())
        if ttl < 0:
            ttl = 1
        redis_client.setex(self.KEY_PREFIX + token, ttl, "1")

    def contains(self, token: str) -> bool:
        return redis_client.exists(self.KEY_PREFIX + token) == 1
