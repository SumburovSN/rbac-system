from dataclasses import dataclass
from app.domain.interfaces.password_hasher import PasswordHasher


@dataclass
class User:
    id: int | None
    name: str
    email: str
    hashed_password: str
    is_active: bool

    @staticmethod
    def create(name: str, email: str, password: str, hasher: PasswordHasher):
        return User(
            id=None,
            name=name,
            email=email,
            hashed_password=hasher.hash(password),
            is_active=True
        )

    def verify_password(self, password: str, hasher: PasswordHasher) -> bool:
        return hasher.verify(password, self.hashed_password)
