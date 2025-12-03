from abc import ABC, abstractmethod
from typing import List
from app.domain.role import Role

class RoleRepository(ABC):

    @abstractmethod
    def create(self, role: Role) -> Role:
        pass

    @abstractmethod
    def get_by_id(self, role_id: int) -> Role | None:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Role | None:
        pass

    @abstractmethod
    def get_all(self) -> List[Role]:
        pass

    @abstractmethod
    def update(self, role: Role, data: dict) -> Role:
        pass
