from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class ProductCreateRequest(BaseModel):
    name: str = Field(..., max_length=255)
    sku: str = Field(..., max_length=100)
    price: float = Field(..., gt=0.0)
    quantity: int = Field(..., ge=0)

class ProductResponse(BaseModel):
    id: UUID
    name: str
    sku: str
    price: float
    quantity: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
