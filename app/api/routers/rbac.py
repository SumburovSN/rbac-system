from fastapi import APIRouter, Depends, HTTPException
from app.use_cases.permission import Permission
from app.api.schemas.rbac import (
    RoleCreate, RoleUpdate, RoleOut,
    BusinessElementCreate, BusinessElementUpdate, BusinessElementOut,
    AccessRoleRuleCreate, AccessRoleRuleUpdate, AccessRoleRuleOut, AccessRoleRuleWithNamesOut, UserRoleOut,
    UserRoleCreate, UserRoleWithNamesOut, UserRoleUpdate, AccessFullOut
)
from app.api.dependencies import (
    get_role_service, get_business_element_service, get_access_rule_service,
    get_current_user, get_user_role_service, get_permission_service
)

router = APIRouter(prefix="/rbac", tags=["RBAC"])

# ====================================================
#                       Observe All
# ====================================================
@router.get("/full", response_model=list[AccessFullOut])
async def get_full_access_relations(
    email: str | None = None,
    user_name: str | None = None,
    role_name: str | None = None,
    element_code: str | None = None,
    page: int = 1,
    size: int = 20,
    service=Depends(get_access_rule_service),
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service),
):
    if not permission.has_permission(user.id, "users", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")

    return service.get_full(email, user_name, role_name, element_code, page, size)

# ====================================================
#                       ROLES
# ====================================================

@router.post("/roles", response_model=RoleOut)
async def create_role(
    data: RoleCreate,
    service = Depends(get_role_service),
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "users", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        return service.create(data)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/roles", response_model=list[RoleOut])
async def list_roles(
    service = Depends(get_role_service),
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "users", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")
    return service.get_all()


@router.get("/roles/{role_id}", response_model=RoleOut)
async def get_role(
    role_id: int,
    service = Depends(get_role_service),
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "users", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")
    role = service.get(role_id)
    if not role:
        raise HTTPException(404, "Role not found")
    return role


@router.put("/roles/{role_id}", response_model=RoleOut)
async def update_role(
    role_id: int,
    data: RoleUpdate,
    service = Depends(get_role_service),
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "users", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")
    role = service.get(role_id)
    if not role:
        raise HTTPException(404, "Role not found")
    try:
        return service.update(role_id, data)
    except ValueError as e:
        raise HTTPException(400, str(e))

# ====================================================
#                 BUSINESS ELEMENTS
# ====================================================

@router.post("/elements", response_model=BusinessElementOut)
async def create_element(
    data: BusinessElementCreate,
    service = Depends(get_business_element_service),
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "users", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        return service.create(data)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/elements", response_model=list[BusinessElementOut])
async def list_elements(
    service = Depends(get_business_element_service),
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "users", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")
    return service.get_all()


@router.get("/elements/{element_id}", response_model=BusinessElementOut)
async def get_element(
    element_id: int,
    service = Depends(get_business_element_service),
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "users", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")
    element = service.get(element_id)
    if not element:
        raise HTTPException(404, "Element not found")
    return element


@router.put("/elements/{element_id}", response_model=BusinessElementOut)
async def update_element(
    element_id: int,
    data: BusinessElementUpdate,
    service = Depends(get_business_element_service),
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "users", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")
    element = service.get(element_id)
    if not element:
        raise HTTPException(404, "Element not found")
    try:
        return service.update(element_id, data)
    except ValueError as e:
        raise HTTPException(400, str(e))


# ====================================================
#                ACCESS ROLE RULES
# ====================================================

@router.post("/rules", response_model=AccessRoleRuleOut)
async def create_rule(
    data: AccessRoleRuleCreate,
    service = Depends(get_access_rule_service),
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "users", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        return service.create(data)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/rules", response_model=list[AccessRoleRuleWithNamesOut])
async def list_rules(
    service = Depends(get_access_rule_service),
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "users", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")
    return service.get_all()


@router.get("/rules/{rule_id}", response_model=AccessRoleRuleOut)
async def get_rule(
    rule_id: int,
    service = Depends(get_access_rule_service),
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "users", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")
    rule = service.get(rule_id)
    if not rule:
        raise HTTPException(404, "Rule not found")
    return rule


@router.put("/rules/{rule_id}", response_model=AccessRoleRuleOut)
async def update_rule(
    rule_id: int,
    data: AccessRoleRuleUpdate,
    service = Depends(get_access_rule_service),
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "users", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")
    rule = service.get(rule_id)
    if not rule:
        raise HTTPException(404, "Rule not found")
    try:
        return service.update(rule_id, data)
    except ValueError as e:
        raise HTTPException(400, str(e))


# ====================================================
#                    USER ROLE
# ====================================================

@router.post("/user_roles", response_model=UserRoleOut)
async def create_user_role(
    data: UserRoleCreate,
    service = Depends(get_user_role_service),
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "users", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        return service.create(data)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/user_roles", response_model=list[UserRoleWithNamesOut])
async def list_all_user_roles(
    service = Depends(get_user_role_service),
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "users", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")
    domain_user_roles = service.get_all()
    return [UserRoleWithNamesOut(
        id=user_role.id,
        user_id=user_role.user_id,
        role_id=user_role.role_id,
        user_name=user_role.user_name,
        role_name=user_role.role_name,
        )
        for user_role in domain_user_roles]


@router.get("/user_roles/{user_id}", response_model=list[UserRoleWithNamesOut])
async def get_user_role(
    user_id: int,
    service = Depends(get_user_role_service),
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "users", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")
    domain_user_roles = service.get_by_user(user_id)
    return [UserRoleWithNamesOut(
        id=user_role.id,
        user_id=user_role.user_id,
        role_id=user_role.role_id,
        user_name=user_role.user_name,
        role_name=user_role.role_name,
    )
        for user_role in domain_user_roles]


@router.put("/user_role/{user_role_id}", response_model=UserRoleOut)
async def update_rule(
    user_role_id: int,
    data: UserRoleUpdate,
    service = Depends(get_user_role_service),
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "users", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")
    user_role = service.get(user_role_id)
    if not user_role:
        raise HTTPException(404, "User Role not found")
    try:
        return service.update(user_role_id, data)
    except ValueError as e:
        raise HTTPException(400, str(e))
