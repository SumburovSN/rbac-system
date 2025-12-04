from fastapi import HTTPException, APIRouter, Depends

from app.api.dependencies import get_current_user, get_permission_service
from app.api.schemas.orders import Order, OrderCreate, OrderUpdate
from app.infrastructure.mock_repositories.orders_repo import MockOrdersRepository
from app.use_cases.permission import Permission

router = APIRouter(prefix="/orders", tags=["Orders"])
repo = MockOrdersRepository()

@router.get("/orders_list", response_model=list[Order])
async def get_goods(
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "orders", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")
    return repo.get_all()

@router.get("/get_order/{orders_id}", response_model=Order)
async def get_goods_by_id(order_id: int,
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "orders", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")
    item = repo.get_by_id(order_id)
    if not item:
        raise HTTPException(404, "Item not found")
    return item

@router.post("/create", response_model=Order)
async def create_goods(item: OrderCreate,
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "orders", "create"):
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        return repo.create(item)
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.put("/update/{order_id}", response_model=Order)
async def update_goods(order_id: int,
    data: OrderUpdate,
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "orders", "update"):
        raise HTTPException(status_code=403, detail="Forbidden")
    updated = repo.update(order_id, data)
    if not updated:
        raise HTTPException(404, "Item not found")
    return updated

@router.delete("/delete/{orders_id}")
async def delete_goods(order_id: int,
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "orders", "delete"):
        raise HTTPException(status_code=403, detail="Forbidden")
    ok = repo.delete(order_id)
    if not ok:
        raise HTTPException(404, "Item not found")
    return {"message": "Deleted"}