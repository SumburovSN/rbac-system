from fastapi import Depends, HTTPException, status

from app.api.dependencies import get_current_user, get_permission_service
from app.use_cases.permission import Permission


class PermissionChecker:
    """
    Использование:
    @router.get("/users", dependencies=[permission.read("users")])
    """

    def require(self, element_code: str, permission_type: str):
        async def dependency(
            user=Depends(get_current_user),
            perm: Permission = Depends(get_permission_service)
        ):
            # Wildcard all
            if perm.has_permission(user.id, "all", permission_type):
                return

            # Конкретный элемент
            if perm.has_permission(user.id, element_code, permission_type):
                return

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden"
            )

        return Depends(dependency)

    def read(self, element_code: str):
        return self.require(element_code, "read")

    def create(self, element_code: str):
        return self.require(element_code, "create")

    def update(self, element_code: str):
        return self.require(element_code, "update")

    def delete(self, element_code: str):
        return self.require(element_code, "delete")


permission = PermissionChecker()
