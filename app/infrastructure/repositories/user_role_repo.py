from sqlalchemy.orm import Session
from app.domain.repositories.user_role_repository import UserRoleRepository
from app.domain.user_role import UserRole as DomainUserRole
from app.infrastructure.db.models.user_role import UserRole as DbUserRole
from app.infrastructure.db.models.user import User as DbUser
from app.infrastructure.db.models.role import Role as DbRole


class UserRoleRepositoryImpl(UserRoleRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_role: DomainUserRole) -> DomainUserRole:
        db_user_role = DbUserRole(user_id=user_role.user_id, role_id=user_role.role_id)
        self.db.add(db_user_role)
        self.db.commit()
        self.db.refresh(db_user_role)
        return self._to_domain(db_user_role)

    def get_by_user(self, user_id: int) -> list[DomainUserRole]:
        db_user_roles = (
            self.db.query(DbUserRole, DbUser.name, DbRole.name)
            .join(DbUser, DbUser.id == DbUserRole.user_id)
            .join(DbRole, DbRole.id == DbUserRole.role_id)
            .filter(DbUserRole.user_id == user_id)
            .all()
        )
        for user_role in db_user_roles:
            print(user_role[0], user_role[1])
        return [self._to_domain_name(user_role) for user_role in db_user_roles]

    def get_all(self) -> list[DomainUserRole]:
        db_user_roles = (
            self.db.query(DbUserRole, DbUser.name, DbRole.name)
            .join(DbUser, DbUser.id == DbUserRole.user_id)
            .join(DbRole, DbRole.id == DbUserRole.role_id)
            .all()
        )
        return [self._to_domain_name(user_role) for user_role in db_user_roles]

    def update(self, user_role: DomainUserRole, data: dict) -> DomainUserRole:
        db_user_role = self.get_by_user_role_id(user_role.user_id, user_role.role_id)
        if not db_user_role:
            raise ValueError("UserRole not found")
        for k, v in data.items():
            setattr(db_user_role, k, v)
        self.db.commit()
        self.db.refresh(db_user_role)
        return self._to_domain(db_user_role)

    def get_by_user_role_id(self, user_id: int, role_id: int) -> DomainUserRole | None:
        db_user_role = (
            self.db.query(DbUserRole).filter(DbUserRole.user_id == user_id, DbUserRole.role_id == role_id).
            first()
        )
        return self._to_domain(db_user_role) if db_user_role else None

    def get_by_id(self, user_role_id: int) -> DomainUserRole | None:
        db_user_role = (
            self.db.query(DbUserRole).filter(DbUserRole.id == user_role_id).first()
        )
        return self._to_domain(db_user_role) if db_user_role else None

    @staticmethod
    def _to_domain_name(db_user_role) -> DomainUserRole:
        db_obj, user_name, role_name = db_user_role

        return DomainUserRole(
            id=db_obj.id,
            user_id=db_obj.user_id,
            role_id=db_obj.role_id,
            user_name=user_name,
            role_name=role_name,
        )

    @staticmethod
    def _to_domain(db_user_role) -> DomainUserRole:
        return DomainUserRole(
            id=db_user_role.id,
            user_id=db_user_role.user_id,
            role_id=db_user_role.role_id,
        )
