from app.domain.user_role import UserRole as DomainUserRole
from app.domain.repositories.user_role_repository import UserRoleRepository
from app.api.schemas.rbac import UserRoleCreate, UserRoleUpdate


class UserRoleService:
    def __init__(self, repo: UserRoleRepository):
        self.repo = repo

    def create(self, data: UserRoleCreate) -> DomainUserRole:
        # Проверка уникальности назначения роли пользователю
        existing = self.repo.get_by_user_role_id(data.user_id, data.role_id)
        if existing:
            raise ValueError("Role is already assigned to user")
        domain_user_role = DomainUserRole.create(user_id=data.user_id, role_id=data.role_id)
        return self.repo.create(domain_user_role)

    def get_all(self) -> list[DomainUserRole]:
        return self.repo.get_all()

    def get_by_user(self, user_id: int) -> list[DomainUserRole]:
        print("service", user_id)
        return self.repo.get_by_user(user_id)

    def update(self, role_id: int, data: UserRoleUpdate) -> DomainUserRole:
        role = self.repo.get_by_id(role_id)
        if not role:
            raise ValueError("Role not found")
        update_data = data.model_dump(exclude_unset=True)
        return self.repo.update(role, update_data)
