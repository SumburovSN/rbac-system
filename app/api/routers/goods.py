from fastapi import HTTPException, APIRouter, Depends

from app.api.dependencies import get_current_user, get_permission_service
from app.api.schemas.goods import Good, GoodCreate, GoodUpdate
from app.infrastructure.mock_repositories.goods_repo import MockGoodsRepository
from app.use_cases.permission import Permission

router = APIRouter(prefix="/goods", tags=["Goods"])
repo = MockGoodsRepository()

@router.get("/goods_list", response_model=list[Good])
async def get_goods(
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "goods", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")
    return repo.get_all()

@router.get("/get_good/{good_id}", response_model=Good)
async def get_goods_by_id(good_id: int,
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "goods", "read"):
        raise HTTPException(status_code=403, detail="Forbidden")
    item = repo.get_by_id(good_id)
    if not item:
        raise HTTPException(404, "Item not found")
    return item

@router.post("/create", response_model=Good)
async def create_goods(item: GoodCreate,
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "goods", "create"):
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        return repo.create(item)
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.put("/update/{good_id}", response_model=Good)
async def update_goods(good_id: int,
    data: GoodUpdate,
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "goods", "update"):
        raise HTTPException(status_code=403, detail="Forbidden")
    updated = repo.update(good_id, data)
    if not updated:
        raise HTTPException(404, "Item not found")
    return updated

@router.delete("/delete/{good_id}")
async def delete_goods(good_id: int,
    user=Depends(get_current_user),
    permission: Permission = Depends(get_permission_service)
):
    if not permission.has_permission(user.id, "goods", "delete"):
        raise HTTPException(status_code=403, detail="Forbidden")
    ok = repo.delete(good_id)
    if not ok:
        raise HTTPException(404, "Item not found")
    return {"message": "Deleted"}
