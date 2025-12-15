from uuid import UUID
import redis.asyncio as aioredis
from fastapi import Request
from app.infrastructure.redis_client import redis_client
from app.domain.repositories.session_repository_redis import SessionRepositoryRedis
from app.use_cases.session_service import SessionService
from app.api.session_cookie import SessionCookieManager
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.domain.user import User
from app.infrastructure.db.db_session import SessionLocal
from app.domain.interfaces.security.jwt_provider_impl import JWTTokenProvider
from app.infrastructure.repositories.user_role_repo import UserRoleRepositoryImpl
from app.use_cases.permission import Permission
from app.use_cases.user_role_service import UserRoleService
from app.use_cases.users_service import UserService
from app.infrastructure.repositories.user_repo import UserRepositoryImpl
from app.use_cases.role_service import RoleService
from app.infrastructure.repositories.role_repo import RoleRepositoryImpl
from app.use_cases.business_element_service import BusinessElementService
from app.infrastructure.repositories.business_element_repo import BusinessElementRepositoryImpl
from app.use_cases.access_role_rule_service import AccessRoleRuleService
from app.infrastructure.repositories.access_role_rule_repo import AccessRoleRuleRepositoryImpl


# bearer_scheme = HTTPBearer()

def get_redis_client() -> aioredis.Redis:
    return redis_client


def get_session_repository(redis_client: aioredis.Redis = Depends(get_redis_client)):
    return SessionRepositoryRedis(redis_client)


async def get_session_service(repo: SessionRepositoryRedis = Depends(get_session_repository)):
    # можно брать ttl из настроек, здесь дефолт 3600
    return SessionService(repo, session_ttl_seconds=3600)


def get_cookie_manager():
    # secure False for local dev; set env/config in prod
    return SessionCookieManager(secure=False, samesite="lax")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    session_service: SessionService = Depends(get_session_service)
) -> User:

    token = get_cookie_manager().get_cookie(request)
    if not token:
        raise HTTPException(401, "Missing cookie")

    jwt_provider = JWTTokenProvider()
    payload = jwt_provider.decode(token)
    if payload is None:
        raise HTTPException(401, "Invalid or expired token")

    session_id = payload.get("sid")
    if not session_id:
        raise HTTPException(401, "Invalid token (no sid)")

    session = await session_service.get_session(UUID(session_id))
    if not session:
        raise HTTPException(401, "Session expired")

    user_repo = UserRepositoryImpl(db)
    user = user_repo.get_by_id(session.user_id)

    if not user:
        raise HTTPException(401, "User not found")

    return user


def get_user_service(db: Session = Depends(get_db)):
    return UserService(UserRepositoryImpl(db))


def get_role_service(db: Session = Depends(get_db)):
    return RoleService(RoleRepositoryImpl(db))


def get_permission_service(db: Session = Depends(get_db)):
    return Permission(db, AccessRoleRuleRepositoryImpl(db), UserRoleRepositoryImpl(db),
                      BusinessElementRepositoryImpl(db))


def get_business_element_service(db: Session = Depends(get_db)):
    return BusinessElementService(BusinessElementRepositoryImpl(db))


def get_access_rule_service(db: Session = Depends(get_db)):
    return AccessRoleRuleService(AccessRoleRuleRepositoryImpl(db))


def get_user_role_service(db: Session = Depends(get_db)):
    return UserRoleService(UserRoleRepositoryImpl(db))
