from dataclasses import dataclass
from datetime import datetime, UTC
from uuid import UUID


@dataclass
class Session:
    uuid: UUID
    user_id: int
    created_at: datetime
    expires_at: datetime
    ip: str | None = None
    user_agent: str | None = None

    @property
    def is_expired(self) -> bool:
        return datetime.now(UTC) > self.expires_at
