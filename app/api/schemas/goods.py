from pydantic import BaseModel


class Good(BaseModel):
    id: int
    name: str
    price: float


class GoodCreate(BaseModel):
    name: str
    price: float


class GoodUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
