from pydantic import BaseModel

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    user_id: int
    items: list[OrderItemCreate]

class OrderResponseItem(BaseModel):
    product_id: int
    quantity: int

class OrderResponse(BaseModel):
    id: int
    user_id: int
    created_at: str
    items: list[OrderResponseItem]

    class Config:
        from_attributes = True