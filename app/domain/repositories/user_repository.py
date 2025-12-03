from abc import ABC, abstractmethod
from typing import List

from app.domain.user import User

class UserRepository(ABC):

    @abstractmethod
    def create(self, data: dict) -> User | None:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def update(self, user: User, data: dict) -> User | None:
        pass

    @abstractmethod
    def delete(self, user: User) -> None:
        pass

