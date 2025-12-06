from app.domain.interfaces.password_hasher import PasswordHasher
import bcrypt

class BcryptPasswordHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify(self, password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed.encode())

# from passlib.context import CryptContext
# from app.domain.interfaces.password_hasher import PasswordHasher
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# class BcryptPasswordHasher(PasswordHasher):
#     def hash(self, password: str) -> str:
#         return pwd_context.hash(password)
#
#     def verify(self, password: str, hashed: str) -> bool:
#         return pwd_context.verify(password, hashed)
