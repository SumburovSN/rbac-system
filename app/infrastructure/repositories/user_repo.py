from sqlalchemy.orm import Session
from app.domain.repositories.user_repository import UserRepository
from app.domain.user import User as DomainUser
from app.infrastructure.db.models.user import User as DbUser


class UserRepositoryImpl(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: DomainUser) -> DomainUser | None:
        db_user = DbUser(
            name=user.name,
            email=user.email,
            hashed_password=user.hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return self._to_domain(db_user)

    def get_by_email(self, email: str) -> DomainUser | None:
        db_user = self.db.query(DbUser).filter(DbUser.email == email).first()
        if not db_user:
            return None
        return self._to_domain(db_user)

    def get_by_id(self, user_id: int):
        db_user = self.db.query(DbUser).filter(DbUser.id == user_id).first()
        # db_user = self.db.get(DbUser, user_id)
        if not db_user:
            return None
        return self._to_domain(db_user)

    def get_all(self) -> list[DomainUser]:
        db_users = self.db.query(DbUser).all()
        return [self._to_domain(u) for u in db_users]

    def update(self, user: DomainUser, data: dict) -> DomainUser | None:
        db_user = self.db.get(DbUser, user.id)
        if not db_user:
            raise ValueError("User not found")
        for key, value in data.items():
            setattr(db_user, key, value)
        self.db.commit()
        self.db.refresh(db_user)
        return self._to_domain(db_user)

    def delete(self, user: DomainUser) -> None:
        db_user = self.db.get(DbUser, user.id)
        if not db_user:
            raise ValueError("User not found")
        db_user.is_active = False
        self.db.commit()

    @staticmethod
    def _to_domain(db_user: DbUser) -> DomainUser:
        """Конвертация ORM → Domain"""
        return DomainUser(
            id=db_user.id,
            name=db_user.name,
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            is_active=db_user.is_active
        )
