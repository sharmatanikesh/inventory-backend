from uuid import UUID
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class OrderItemRequest(BaseModel):
    product_id: UUID
    quantity: int = Field(..., gt=0)

class OrderCreateRequest(BaseModel):
    customer_id: UUID
    items: List[OrderItemRequest]

class OrderItemResponse(BaseModel):
    id: UUID
    order_id: UUID
    product_id: UUID
    quantity: int
    unit_price: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class OrderResponse(BaseModel):
    id: UUID
    customer_id: UUID
    total_amount: float
    status: str
    created_at: datetime
    updated_at: datetime
    cancelled_at: Optional[datetime] = None
    items: List[OrderItemResponse] = []

    model_config = ConfigDict(from_attributes=True)
