from datetime import datetime, timedelta, timezone
from jose import jwt
from app.config import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.domain.interfaces.token_provider import TokenProvider


class JWTTokenProvider(TokenProvider):
    def encode(self, data: dict) -> str:
        """Создаёт JWT токен с exp + payload."""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, JWT_SECRET_KEY, JWT_ALGORITHM)

    def decode(self, token: str) -> dict | None:
        """Проверяет и декодирует JWT."""
        try:
            payload = jwt.decode(
                token,
                JWT_SECRET_KEY,
                algorithms=[JWT_ALGORITHM]
            )
            return payload
        except Exception as e:
            print("DECODE ERROR:", e)
            return None
