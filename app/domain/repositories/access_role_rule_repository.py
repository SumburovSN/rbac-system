from abc import ABC, abstractmethod
from app.domain.access_role_rule import AccessRoleRule

class AccessRoleRuleRepository(ABC):

    @abstractmethod
    def create(self, rule: AccessRoleRule) -> AccessRoleRule:
        pass

    @abstractmethod
    def get_by_id(self, rule_id: int) -> AccessRoleRule | None:
        pass

    @abstractmethod
    def get_all(self) -> list[AccessRoleRule]:
        pass

    @abstractmethod
    def get_by_role_and_element(self, role_id: int, element_id: int) -> AccessRoleRule | None:
        pass

    @abstractmethod
    def update(self, rule: AccessRoleRule, data: dict) -> AccessRoleRule:
        pass
