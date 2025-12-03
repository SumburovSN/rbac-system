from pydantic import BaseModel


# ===================== ROLE =====================

class RoleCreate(BaseModel):
    name: str
    description: str | None = None


class RoleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class RoleOut(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True


# =============== BUSINESS ELEMENT =================

class BusinessElementCreate(BaseModel):
    code: str
    name: str


class BusinessElementUpdate(BaseModel):
    code: str | None = None
    name: str | None = None


class BusinessElementOut(BaseModel):
    id: int
    code: str
    name: str

    class Config:
        from_attributes = True


# ============ ACCESS ROLE RULE ====================

class AccessRoleRuleCreate(BaseModel):
    role_id: int
    element_id: int
    read_permission: bool = False
    # read_all_permission: bool = False
    create_permission: bool = False
    update_permission: bool = False
    # update_all_permission: bool = False
    delete_permission: bool = False
    # delete_all_permission: bool = False


class AccessRoleRuleUpdate(BaseModel):
    read_permission: bool | None = None
    # read_all_permission: bool | None = None
    create_permission: bool | None = None
    update_permission: bool | None = None
    # update_all_permission: bool | None = None
    delete_permission: bool | None = None
    # delete_all_permission: bool | None = None


class AccessRoleRuleOut(BaseModel):
    id: int
    role_id: int
    element_id: int
    read_permission: bool
    create_permission: bool
    update_permission: bool
    delete_permission: bool

    class Config:
        from_attributes = True


class AccessRoleRuleWithNamesOut(BaseModel):
    id: int
    role_id: int
    role_name: str  # дополнительное поле для имени роли
    element_id: int
    element_code: str  # дополнительное поле для кода элемента
    read_permission: bool
    create_permission: bool
    update_permission: bool
    delete_permission: bool

    class Config:
        from_attributes = True


# ============ USER ROLE RULE ====================

class UserRoleCreate(BaseModel):
    id: int | None = None
    user_id: int
    role_id: int


class UserRoleUpdate(BaseModel):
    user_id: int
    role_id: int


class UserRoleOut(BaseModel):
    id: int | None
    user_id: int
    role_id: int

    class Config:
        from_attributes = True

class UserRoleWithNamesOut(BaseModel):
    id: int | None
    user_id: int
    role_id: int
    user_name: str
    role_name: str

    class Config:
        from_attributes = True
