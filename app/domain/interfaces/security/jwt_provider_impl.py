from datetime import datetime, timedelta, UTC
# from jose import jwt
import jwt
from app.config import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.domain.interfaces.token_provider import TokenProvider


class JWTTokenProvider(TokenProvider):
    def __init__(self, secret: str = JWT_SECRET_KEY, algorithm: str = JWT_ALGORITHM,
                 expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES):
        self.secret = secret
        self.algorithm = algorithm
        self.ttl_seconds = expire_minutes * 60

    # def encode(self, session_id: str, ttl_seconds: int = 3600) -> str:
    def encode(self, session_id: str) -> str:
        now = datetime.now(UTC)
        payload = {
            "sid": session_id,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(seconds=self.ttl_seconds)).timestamp()),
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def decode(self, token: str) -> dict | None:
        try:
            return jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None


# class JWTTokenProvider(TokenProvider):
#     def encode(self, data: dict) -> str:
#         """Создаёт JWT токен с exp + payload."""
#         to_encode = data.copy()
#         expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#         to_encode.update({"exp": expire})
#         return jwt.encode(to_encode, JWT_SECRET_KEY, JWT_ALGORITHM)
#
#     def decode(self, token: str) -> dict | None:
#         """Проверяет и декодирует JWT."""
#         try:
#             payload = jwt.decode(
#                 token,
#                 JWT_SECRET_KEY,
#                 algorithms=[JWT_ALGORITHM]
#             )
#             return payload
#         except Exception as e:
#             print("DECODE ERROR:", e)
#             return None
