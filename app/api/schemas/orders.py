from pydantic import BaseModel


class Order(BaseModel):
    id: int
    manufacturer: str
    description: str


class OrderCreate(BaseModel):
    manufacturer: str
    description: str


class OrderUpdate(BaseModel):
    manufacturer: str | None = None
    description: str | None = None
