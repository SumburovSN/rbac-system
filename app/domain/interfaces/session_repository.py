from abc import ABC, abstractmethod
from uuid import UUID
from app.domain.session import Session


class SessionRepository(ABC):
    @abstractmethod
    def add(self, session: Session) -> None:
        """Сохраняет новую сессию в хранилище."""
        pass

    @abstractmethod
    def get(self, session_id: UUID) -> Session | None:
        """Возвращает сессию по её UUID, либо None, если не найдена."""
        pass

    @abstractmethod
    def delete(self, session_id: UUID) -> None:
        """Удаляет сессию (используется при логауте)."""
        pass
