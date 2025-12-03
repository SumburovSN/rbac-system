from abc import ABC, abstractmethod
from app.domain.user_role import UserRole

class UserRoleRepository(ABC):

    @abstractmethod
    def create(self, user_role: UserRole) -> UserRole:
        pass

    @abstractmethod
    def get_by_user(self, user_id: int) -> list[UserRole]:
        pass

    @abstractmethod
    def get_all(self) -> list[UserRole]:
        pass

    @abstractmethod
    def update(self, user_role: UserRole, data: dict) -> UserRole:
        pass

    @abstractmethod
    def get_by_user_role_id(self, user_id: int, role_id: int) -> UserRole | None:
        pass

    @abstractmethod
    def get_by_id(self, user_role_id: int) -> UserRole | None:
        pass
