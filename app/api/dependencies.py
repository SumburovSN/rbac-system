from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.domain.user import User
from app.infrastructure.db.session import SessionLocal
from app.domain.interfaces.security.jwt_provider_impl import JWTTokenProvider
from app.infrastructure.repositories.user_role_repo import UserRoleRepositoryImpl
from app.use_cases.blacklist_service import TokenBlacklistService
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


bearer_scheme = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials

    blacklist = get_blacklist_service()
    if blacklist.contains(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked"
        )

    token_provider = JWTTokenProvider()
    payload = token_provider.decode(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    if payload.get("exp") is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_repo = UserRepositoryImpl(db)
    user = user_repo.get_by_id(payload["sub"])
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
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

def get_blacklist_service():
    return TokenBlacklistService()
