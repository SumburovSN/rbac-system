from pydantic import BaseModel, ConfigDict, EmailStr


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

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)


# ============ ACCESS ROLE RULE ====================

class AccessRoleRuleCreate(BaseModel):
    role_id: int
    element_id: int
    read_permission: bool = False
    create_permission: bool = False
    update_permission: bool = False
    delete_permission: bool = False


class AccessRoleRuleUpdate(BaseModel):
    read_permission: bool | None = None
    create_permission: bool | None = None
    update_permission: bool | None = None
    delete_permission: bool | None = None


class AccessRoleRuleOut(BaseModel):
    id: int
    role_id: int
    element_id: int
    read_permission: bool
    create_permission: bool
    update_permission: bool
    delete_permission: bool

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)


class UserRoleWithNamesOut(BaseModel):
    id: int | None
    user_id: int
    role_id: int
    user_name: str
    role_name: str

    model_config = ConfigDict(from_attributes=True)


class UserAccessInfo(BaseModel):
    user_id: int
    user_name: str
    email: EmailStr
    role_name: str

    model_config = ConfigDict(from_attributes=True)


class AccessFullOut(BaseModel):
    user_id: int
    user_email: str
    user_name: str
    role_name: str
    role_description: str | None = None
    element_code: str
    element_name: str
    create: bool
    read: bool
    update: bool
    delete: bool

    model_config = ConfigDict(from_attributes=True)


