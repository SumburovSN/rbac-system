from app.api.schemas.auth import UserOut
from app.domain.interfaces.security.jwt_provider_impl import JWTTokenProvider
from app.domain.repositories.user_repository import UserRepository
from app.domain.user import User as DomainUser
from app.domain.interfaces.security.password_hasher_impl import BcryptPasswordHasher

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
        self.hasher = BcryptPasswordHasher()
        self.token_provider = JWTTokenProvider()

    def register(self, name: str, email: str, password: str) -> str:
        # Проверка на уникальность email
        existing = self.repo.get_by_email(email)
        if existing:
            raise ValueError("User already registered")
        # Создание доменной сущности
        saved_user = DomainUser.create(name=name, email=email, password=password, hasher=self.hasher)
        # Сохранение
        self.repo.create(saved_user)
        # Генерируем JWT
        return self.token_provider.encode({"sub": str(saved_user.id)})

    def login(self, email: str, password: str) -> str:
        user = self.repo.get_by_email(email)
        if not user:
            raise ValueError("User not found")
        if not user.is_active:
            raise ValueError("Account is deleted")
        if not user.verify_password(password, hasher=self.hasher):
            raise ValueError("Invalid credentials")
        # Генерируем JWT
        return self.token_provider.encode({"sub": str(user.id)})

    def get_users_list(self) -> list[UserOut]:
        domain_users = self.repo.get_all()
        return [UserOut.model_validate(user) for user in domain_users]

    def get_user(self, user_id: int) -> UserOut | None:
        user = self.repo.get_by_id(user_id)
        return UserOut.model_validate(user) if user else None

    def update_user(self, user_id: int, data) -> DomainUser:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        update_data = data.dict(exclude_unset=True)
        # Проверка на уникальность email
        existing = self.repo.get_by_email(update_data["email"])
        if existing:
            if existing.id != user_id:
                raise ValueError("User with the same email already registered")
        return self.repo.update(user, update_data)

    def delete_user(self, user_id: int) -> None:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        self.repo.delete(user)
