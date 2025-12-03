from sqlalchemy.orm import Session
from app.domain.repositories.access_role_rule_repository import AccessRoleRuleRepository
from app.domain.repositories.user_role_repository import UserRoleRepository
from app.domain.repositories.business_element_repository import BusinessElementRepository
from app.infrastructure.db.models.access_role_rule import AccessRoleRule
from app.infrastructure.db.models.business_element import BusinessElement
from app.infrastructure.db.models.user_role import UserRole


class Permission:
    def __init__(self, db: Session, rule_repo: AccessRoleRuleRepository, user_role_repo: UserRoleRepository,
                 element_repo: BusinessElementRepository):
        self.db = db
        self.rule_repo = rule_repo
        self.user_role_repo = user_role_repo
        self.element_repo = element_repo

    def permission_found(self, user_id: int, element_code: str, permission_type: str) -> bool:
        permission_column = {
            "read": AccessRoleRule.read_permission,
            "create": AccessRoleRule.create_permission,
            "update": AccessRoleRule.update_permission,
            "delete": AccessRoleRule.delete_permission,
        }.get(permission_type)

        if permission_column is None:
            raise ValueError(f"Unknown permission type: {permission_type}")

        # Один оптимальный запрос
        rule = (
            self.db.query(AccessRoleRule)
            .join(UserRole, UserRole.role_id == AccessRoleRule.role_id)
            .join(BusinessElement, BusinessElement.id == AccessRoleRule.element_id)
            .filter(
                UserRole.user_id == user_id,
                BusinessElement.code == element_code,
                permission_column == True,  # нужное разрешение
            )
            .first()
        )

        return rule is not None

    def has_permission(self, user_id: int, element_code: str, permission_type: str) -> bool:
        if self.permission_found(user_id, "all", permission_type):
            return True
        elif self.permission_found(user_id, element_code, permission_type):
            return True
        else:
            return False