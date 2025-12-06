from sqlalchemy.orm import Session
from app.domain.repositories.access_role_rule_repository import AccessRoleRuleRepository
from app.domain.access_role_rule import AccessRoleRule as DomainRule
from app.infrastructure.db.models.access_role_rule import AccessRoleRule as DbRule
from app.infrastructure.db.models.business_element import BusinessElement as DbBusinessElement
from app.infrastructure.db.models.role import Role as DbRole
from app.infrastructure.db.models.user import User as DbUser
from app.infrastructure.db.models.user_role import UserRole as DbUserRole


class AccessRoleRuleRepositoryImpl(AccessRoleRuleRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, rule: DomainRule) -> DomainRule:
        db_rule = DbRule(role_id=rule.role_id, element_id=rule.element_id, read_permission=rule.read_permission,
                         create_permission=rule.create_permission, update_permission=rule.create_permission,
                         delete_permission=rule.delete_permission)
        self.db.add(db_rule)
        self.db.commit()
        self.db.refresh(db_rule)
        return self._to_domain((db_rule, None, None))

    def get_by_id(self, rule_id: int) -> DomainRule | None:
        db_rule = self.db.get(DbRule, rule_id)
        return self._to_domain((db_rule, None, None)) if db_rule else None

    def get_all(self) -> list[DomainRule]:
        # Выполняем JOIN для получения всех данных в одном запросе
        db_rules = (
            self.db.query(DbRule, DbRole.name, DbBusinessElement.code)
            .join(DbRole, DbRole.id == DbRule.role_id)
            .join(DbBusinessElement, DbBusinessElement.id == DbRule.element_id)
            .all()
        )
        return [self._to_domain(rule) for rule in db_rules]

    def get_by_role_and_element(self, role_id: int, element_id: int) -> DomainRule | None:
        db_rule = (
            self.db.query(DbRule, DbRole.name, DbBusinessElement.code).join(DbRole, DbRole.id == DbRule.role_id)
            .join(DbBusinessElement, DbBusinessElement.id == DbRule.element_id)
            .filter(DbRule.role_id == role_id, DbRule.element_id == element_id).first()
        )
        return self._to_domain(db_rule) if db_rule else None

    def update(self, rule: DomainRule, data: dict) -> DomainRule:
        db_rule = self.db.get(DbRule, rule.id)
        if not db_rule:
            raise ValueError("AccessRule not found")
        for k, v in data.items():
            setattr(db_rule, k, v)
        self.db.commit()
        self.db.refresh(db_rule)
        return self._to_domain((db_rule, None, None))

    def get_full(
            self,
            email: str | None,
            user_name: str | None,
            role_name: str | None,
            element_code: str | None,
            offset: int,
            limit: int
    ):
        query = (
            self.db.query(
                DbUser.id.label("user_id"),
                DbUser.email.label("user_email"),
                DbUser.name.label("user_name"),
                DbRole.name.label("role_name"),
                DbRole.description.label("role_description"),
                DbBusinessElement.code.label("element_code"),
                DbBusinessElement.name.label("element_name"),
                DbRule.create_permission.label("create"),
                DbRule.read_permission.label("read"),
                DbRule.update_permission.label("update"),
                DbRule.delete_permission.label("delete"),
            )
            .select_from(DbUser)
            .join(DbUserRole, DbUserRole.user_id == DbUser.id)
            .join(DbRole, DbRole.id == DbUserRole.role_id)
            .join(DbRule, DbRule.role_id == DbRole.id)
            .join(DbBusinessElement, DbBusinessElement.id == DbRule.element_id)
        )

        # Фильтры (все через AND)
        if email:
            query = query.filter(DbUser.email.ilike(f"%{email}%"))
        if user_name:
            query = query.filter(DbUser.name.ilike(f"%{user_name}%"))
        if role_name:
            query = query.filter(DbRole.name.ilike(f"%{role_name}%"))
        if element_code:
            query = query.filter(DbBusinessElement.code.ilike(f"%{element_code}%"))

        # Пагинация
        query = query.offset(offset).limit(limit)

        return query.all()


    @staticmethod
    def _to_domain(db_rule: DbRule) -> DomainRule:
        db_rule_obj, role_name, element_code = db_rule

        # Преобразуем в доменный объект
        return DomainRule(
            id=db_rule_obj.id,
            role_id=db_rule_obj.role_id,
            element_id=db_rule_obj.element_id,
            read_permission=db_rule_obj.read_permission,
            create_permission=db_rule_obj.create_permission,
            update_permission=db_rule_obj.update_permission,
            delete_permission=db_rule_obj.delete_permission,
            role_name=role_name,
            element_code=element_code,
        )
