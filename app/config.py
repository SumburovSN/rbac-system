import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./rbac_api.db")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret")
JWT_ALGORITHM = "HS256"
COOKIES_MAX_AGE = int(os.getenv("COOKIES_MAX_AGE", 300))
COOKIES_SECURE = False # Это для тестов, но для релиза в .env True
COOKIES_HTTPONLY = os.getenv("COOKIES_HTTPONLY", "true").lower() == "true"
COOKIES_SAME_SITE = os.getenv("COOKIES_SAME_SITE", "lax")
COOKIES_PATH = os.getenv("COOKIES_PATH", "/")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
