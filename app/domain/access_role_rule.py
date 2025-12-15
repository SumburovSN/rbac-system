from dataclasses import dataclass


@dataclass
class AccessRoleRule:
    id: int | None
    role_id: int
    element_id: int
    read_permission: bool
    create_permission: bool
    update_permission: bool
    delete_permission: bool
    role_name: str | None = None  # Дополнительное поле для имени роли
    element_code: str | None = None  # Дополнительное поле для кода элемента

    @staticmethod
    def create(
        role_id: int,
        element_id: int,
        read_permission: bool = False,
        create_permission: bool = False,
        update_permission: bool = False,
        delete_permission: bool = False,
        role_name: str = None,
        element_code: str = None,
    ):
        return AccessRoleRule(
            id=None,
            role_id=role_id,
            element_id=element_id,
            read_permission=read_permission,
            create_permission=create_permission,
            update_permission=update_permission,
            delete_permission=delete_permission,
            role_name=role_name,
            element_code=element_code,
        )
