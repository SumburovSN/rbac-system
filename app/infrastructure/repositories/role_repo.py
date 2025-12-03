from sqlalchemy.orm import Session
from app.domain.repositories.role_repository import RoleRepository
from app.domain.role import Role as DomainRole
from app.infrastructure.db.models.role import Role as DbRole


class RoleRepositoryImpl(RoleRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, role: DomainRole) -> DomainRole:
        db_role = DbRole(name=role.name, description=role.description)
        self.db.add(db_role)
        self.db.commit()
        self.db.refresh(db_role)
        return self._to_domain(db_role)

    def get_by_id(self, role_id: int) -> DomainRole | None:
        db_role = self.db.get(DbRole, role_id)
        return self._to_domain(db_role) if db_role else None

    def get_by_name(self, name: str) -> DomainRole | None:
        db_role = self.db.query(DbRole).filter(DbRole.name == name).first()
        return self._to_domain(db_role) if db_role else None

    def get_all(self) -> list[DomainRole]:
        db_roles = self.db.query(DbRole).all()
        return [self._to_domain(r) for r in db_roles]

    def update(self, role: DomainRole, data: dict) -> DomainRole:
        db_role = self.db.get(DbRole, role.id)
        if not db_role:
            raise ValueError("Role not found")
        for key, value in data.items():
            setattr(db_role, key, value)
        self.db.commit()
        self.db.refresh(db_role)
        return self._to_domain(db_role)

    def _to_domain(self, db: DbRole) -> DomainRole:
        return DomainRole(
            id=db.id,
            name=db.name,
            description=db.description
        )
