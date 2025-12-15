from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, Request, Response
from app.api.schemas.auth import UserRegister, UserLogin, Token, UserOut, UserUpdate
from app.api.session_cookie import SessionCookieManager
from app.domain.interfaces.security.jwt_provider_impl import JWTTokenProvider
from app.use_cases.permission import Permission
from app.use_cases.session_service import SessionService
from app.use_cases.users_service import UserService
from app.api.dependencies import get_user_service, get_current_user, get_permission_service, get_session_service


router = APIRouter(prefix="/auth", tags=["Auth"])

cookie_manager = SessionCookieManager(max_age=3600)


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


@router.post("/login")
async def login(
    data: UserLogin,
    response: Response,
    user_service: UserService = Depends(get_user_service),
    session_service: SessionService = Depends(get_session_service),
):
    # Проверяем логин/пароль
    user = user_service.login(data.email, data.password)
    if not user:
        raise HTTPException(401, "Invalid credentials")

    # Создаем сессию в Redis
    session = await session_service.create_session(
        user_id=user.id,
        ip=None,
        user_agent="browser"
    )

    # Создаем JWT по session.uuid
    jwt_provider = JWTTokenProvider()
    token = jwt_provider.encode(str(session.uuid))

    # Устанавливаем cookie
    cookie_manager.set_cookie(response, token)

    return {"detail": "Logged in", "session_id": session.uuid}



@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    session_service: SessionService = Depends(get_session_service)
):
    token = cookie_manager.get_cookie(request)
    if not token:
        raise HTTPException(401, "No session token")

    jwt_provider = JWTTokenProvider()
    payload = jwt_provider.decode(token)
    if payload is None:
        raise HTTPException(401, "Invalid token")

    session_id = payload.get("sid")
    if session_id:
        await session_service.delete_session(UUID(session_id))

    cookie_manager.delete_cookie(response)

    return {"detail": "Logged out"}


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
