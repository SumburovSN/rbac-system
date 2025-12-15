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

        # redis возвращает bytes → decode
        # decoded = {k.decode(): v.decode() for k, v in data.items()}

        return self._deserialize(data)

    async def delete(self, session_id: UUID) -> None:
        key = self._key(session_id)
        await self.client.delete(key)

# import json
# from datetime import datetime
# from uuid import UUID
# import redis
# from app.domain.interfaces.session_repository import SessionRepository
# from app.domain.session import Session
#
#
# class SessionRepositoryRedis(SessionRepository):
#     """
#     Хранилище сессий в Redis.
#     Ключи: session:{uuid}
#     Значение: JSON
#     TTL автоматически устанавливается по expires_at.
#     """
#
#     def __init__(self, redis_client: redis.Redis):
#         self.redis = redis_client
#
#     def save(self, session: Session) -> None:
#         key = f"session:{session.uuid}"
#
#         value = json.dumps({
#             "uuid": str(session.uuid),
#             "user_id": session.user_id,
#             "created_at": session.created_at.isoformat(),
#             "expires_at": session.expires_at.isoformat(),
#         })
#
#         # TTL (в секундах)
#         ttl = int((session.expires_at - datetime.utcnow()).total_seconds())
#
#         if ttl <= 0:
#             # просроченные сессии не записываем
#             return
#
#         # сохраним значение и TTL сразу
#         self.redis.setex(key, ttl, value)
#
#     def get(self, session_id: UUID) -> Session | None:
#         key = f"session:{session_id}"
#         raw = self.redis.get(key)
#
#         if raw is None:
#             return None
#
#         data = json.loads(raw)
#
#         return Session(
#             uuid=UUID(data["uuid"]),
#             user_id=data["user_id"],
#             created_at=datetime.fromisoformat(data["created_at"]),
#             expires_at=datetime.fromisoformat(data["expires_at"]),
#         )
#
#     def delete(self, session_id: UUID) -> None:
#         key = f"session:{session_id}"
#         self.redis.delete(key)
