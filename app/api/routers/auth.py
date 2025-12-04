from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials
from app.api.schemas.auth import UserRegister, UserLogin, Token, UserOut, UserUpdate
from app.domain.interfaces.security.jwt_provider_impl import JWTTokenProvider
from app.use_cases.permission import Permission
from app.use_cases.users_service import UserService
from app.api.dependencies import get_user_service, get_current_user, get_permission_service, bearer_scheme, \
    get_blacklist_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=Token)
async def register_user(
    data: UserRegister,
    service: UserService = Depends(get_user_service),
    # user=Depends(get_current_user)
):
    try:
        token = service.register(data.name, data.email, data.password)
        return Token(access_token=token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
async def login_user(
    data: UserLogin,
    service: UserService = Depends(get_user_service)
):
    try:
        token = service.login(str(data.email), data.password)
        return Token(access_token=token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user=Depends(get_current_user)
):
    token = credentials.credentials

    token_provider = JWTTokenProvider()
    payload = token_provider.decode(token)

    if payload is None:
        raise HTTPException(status_code=400, detail="Invalid token")

    exp = payload.get("exp")
    if exp is None:
        raise HTTPException(status_code=400, detail="Invalid token")

    blacklist = get_blacklist_service()
    # Добавляем токен в blacklist
    blacklist.add(token, exp)

    return {"detail": "Logged out successfully"}


@router.get("/users_list", response_model=list[UserOut])
async def list_users(
    service: UserService = Depends(get_user_service),
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "users", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")

    return service.get_users_list()


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int,
    service: UserService = Depends(get_user_service),
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if user.id != user_id and not permission.has_permission(user.id, "users", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")

    user = service.get_user(user_id)
    if not user:
        raise HTTPException(404, "Пользователь не найден")

    return user


@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int,
    data: UserUpdate,
    service: UserService = Depends(get_user_service),
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if user.id != user_id and not permission.has_permission(user.id, "users", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(404, "Пользователь не найден")
    try:
        return service.update_user(user_id, data)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not (user.id == user_id or permission.has_permission(user.id, "users", "read")):
        raise HTTPException(status_code=403, detail="Forbidden")
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(404, "Пользователь не найден")
    service.delete_user(user_id)
    return {"status": "deleted"}
