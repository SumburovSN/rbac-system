# from datetime import datetime, timedelta, UTC
# from jose import jwt
import jwt
from app.config import JWT_SECRET_KEY, JWT_ALGORITHM
from app.domain.interfaces.token_provider import TokenProvider


class JWTTokenProvider(TokenProvider):
    def __init__(self, secret: str = JWT_SECRET_KEY, algorithm: str = JWT_ALGORITHM,
                 expire_minutes: int = 0):
        self.secret = secret
        self.algorithm = algorithm
        # self.ttl_seconds = expire_minutes * 60

    # def encode(self, session_id: str, ttl_seconds: int = 3600) -> str:
    def encode(self, session_data: dict) -> str:
        # self.ttl_seconds = session_data[""]
        payload = {
            "sid": session_data["sid"],
            "iat": session_data["iat"],
            "exp": session_data["exp"],
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def decode(self, token: str) -> dict | None:
        try:
            return jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
