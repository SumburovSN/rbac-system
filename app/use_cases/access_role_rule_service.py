from app.domain.access_role_rule import AccessRoleRule as DomainAccessRoleRule
from app.domain.repositories.access_role_rule_repository import AccessRoleRuleRepository
from app.api.schemas.rbac import AccessRoleRuleCreate, AccessRoleRuleUpdate, AccessRoleRuleWithNamesOut


class AccessRoleRuleService:
    def __init__(self, repo: AccessRoleRuleRepository):
        self.repo = repo

    def create(self, data: AccessRoleRuleCreate) -> DomainAccessRoleRule:
        # Проверка уникальности пары (role_id, element_id)
        existing = self.repo.get_by_role_and_element(
            data.role_id, data.element_id
        )
        if existing:
            raise ValueError("Rule for this role and element already exists")
        domain_rule = DomainAccessRoleRule.create(
            role_id=data.role_id, element_id=data.element_id, read_permission=data.read_permission,
            create_permission=data.create_permission, update_permission=data.create_permission,
            delete_permission=data.delete_permission)
        return self.repo.create(domain_rule)

    def get_all(self) -> list[AccessRoleRuleWithNamesOut]:
        # Получаем все правила с ролью и элементом
        domain_rules = self.repo.get_all()

        # Преобразуем в схемы Pydantic для ответа API
        return [AccessRoleRuleWithNamesOut(
            id=rule.id,
            role_id=rule.role_id,
            role_name=rule.role_name,
            element_id=rule.element_id,
            element_code=rule.element_code,
            read_permission=rule.read_permission,
            create_permission=rule.create_permission,
            update_permission=rule.update_permission,
            delete_permission=rule.delete_permission,
        )
            for rule in domain_rules
        ]

    def get(self, rule_id: int) -> DomainAccessRoleRule:
        return self.repo.get_by_id(rule_id)

    def update(self, rule_id: int, data: AccessRoleRuleUpdate) -> DomainAccessRoleRule:
        rule = self.repo.get_by_id(rule_id)
        if not rule:
            raise ValueError("AccessRoleRule not found")

        update_data = data.model_dump(exclude_unset=True)

        # role_id и element_id менять НЕЛЬЗЯ — это первичный ключ правила
        return self.repo.update(rule, update_data)

    def get_full(
            self,
            email: str | None,
            user_name: str | None,
            role_name: str | None,
            element_code: str | None,
            page: int,
            size: int
    ):
        offset = (page - 1) * size
        return self.repo.get_full(email, user_name, role_name, element_code, offset, size)
