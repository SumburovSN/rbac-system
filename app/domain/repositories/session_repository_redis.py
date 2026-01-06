from datetime import datetime, UTC
from uuid import UUID
import redis.asyncio as redis
from app.domain.session import Session
from app.domain.interfaces.session_repository import SessionRepository


class SessionRepositoryRedis(SessionRepository):
    def __init__(self, client: redis.Redis):
        self.client = client
        self.prefix = "session:"

    def _key(self, session_id: UUID) -> str:
        return f"{self.prefix}{session_id}"

    # ---- Helpers ----

    def _serialize(self, session: Session) -> dict:
        """Convert Session → dict для хранения в Redis."""
        return {
            "uuid": str(session.uuid),
            "user_id": str(session.user_id),
            "created_at": session.created_at.isoformat(),
            "expires_at": session.expires_at.isoformat(),
            "ip": session.ip or "",
            "user_agent": session.user_agent or "",
        }

    def _deserialize(self, data: dict) -> Session:
        """Convert dict → Session."""
        return Session(
            uuid=UUID(data["uuid"]),
            user_id=int(data["user_id"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            expires_at=datetime.fromisoformat(data["expires_at"]),
            ip=data.get("ip") or None,
            user_agent=data.get("user_agent") or None,
        )

    # ---- Public methods ----

    async def add(self, session: Session) -> None:
        key = self._key(session.uuid)
        data = self._serialize(session)

        # сохраняем hash
        await self.client.hset(key, mapping=data)

        # выставляем TTL
        ttl_seconds = int((session.expires_at - datetime.now(UTC)).total_seconds())

        if ttl_seconds > 0:
            await self.client.expire(key, ttl_seconds)
        else:
            await self.client.delete(key)  # истекла ещё до сохранения

    async def get(self, session_id: UUID) -> Session | None:
        key = self._key(session_id)
        data = await self.client.hgetall(key)

        if not data:
            return None

        return self._deserialize(data)

    async def delete(self, session_id: UUID) -> None:
        key = self._key(session_id)
        await self.client.delete(key)
