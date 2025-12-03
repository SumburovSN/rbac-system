from passlib.context import CryptContext
from app.domain.interfaces.password_hasher import PasswordHasher

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class BcryptPasswordHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify(self, password: str, hashed: str) -> bool:
        return pwd_context.verify(password, hashed)
