from dataclasses import dataclass


@dataclass
class UserRole:
    id: int | None
    user_id: int
    role_id: int
    user_name: str | None = None
    role_name: str | None = None

    @staticmethod
    def create(user_id: int, role_id: int, user_name: str = None, role_name: str = None):
        return UserRole(id=None,
                        user_id=user_id,
                        role_id=role_id,
                        user_name=user_name,
                        role_name=role_name
                        )
