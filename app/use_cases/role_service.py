from app.domain.role import Role as DomainRole
from app.domain.repositories.role_repository import RoleRepository
from app.api.schemas.rbac import RoleCreate, RoleUpdate


class RoleService:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    def create(self, data: RoleCreate) -> DomainRole:
        # Проверяем уникальность имени роли
        existing = self.repo.get_by_name(data.name)
        if existing:
            raise ValueError("Role with this name already exists")
        domain_role = DomainRole.create(name=data.name, description=data.description)
        return self.repo.create(domain_role)

    def get_all(self) -> list[DomainRole]:
        return self.repo.get_all()

    def get(self, role_id: int) -> DomainRole:
        return self.repo.get_by_id(role_id)

    def update(self, role_id: int, data: RoleUpdate) -> DomainRole:
        role = self.repo.get_by_id(role_id)
        if not role:
            raise ValueError("Role not found")

        update_data = data.model_dump(exclude_unset=True)

        # Проверка уникальности имени
        if "name" in update_data:
            existing = self.repo.get_by_name(update_data["name"])
            if existing and existing.id != role_id:
                raise ValueError("Role with this name already exists")

        return self.repo.update(role, update_data)
