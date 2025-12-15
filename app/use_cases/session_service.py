from datetime import datetime, timedelta, UTC
from uuid import uuid4, UUID

from app.domain.session import Session
from app.domain.interfaces.session_repository import SessionRepository


class SessionService:
    def __init__(self, repo: SessionRepository, session_ttl_seconds: int = 3600):
        """
        :param repo: repository for sessions (Redis)
        :param session_ttl_seconds: session lifetime
        """
        self.repo = repo
        self.session_ttl_seconds = session_ttl_seconds

    async def create_session(
        self,
        user_id: int,
        ip: str | None = None,
        user_agent: str | None = None,
    ) -> Session:
        """Creates and stores a new session"""

        now = datetime.now(UTC)
        session = Session(
            uuid=uuid4(),
            user_id=user_id,
            created_at=now,
            expires_at=now + timedelta(seconds=self.session_ttl_seconds),
            ip=ip,
            user_agent=user_agent,
        )

        await self.repo.add(session)
        return session

    async def get_session(self, session_id: UUID) -> Session | None:
        """Returns session if exists and not expired"""

        session = await self.repo.get(session_id)

        if session is None:
            return None

        # check expiration
        if session.is_expired:
            # auto-remove expired session
            await self.repo.delete(session_id)
            return None

        return session

    async def delete_session(self, session_id: UUID) -> None:
        """Manually deletes a session"""
        await self.repo.delete(session_id)

    async def logout_user(self, user_id: int):
        """
        Deletes ALL active user sessions.
        Useful for 'logout all devices'.
        """
        # optional: implement repo.get_sessions_by_user(user_id)
        # for now we leave a stub
        pass
