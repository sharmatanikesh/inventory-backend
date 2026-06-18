from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from app.service.interfaces.order_service import OrderServiceInterface
from app.routers.deps import get_order_service

router = APIRouter()

class OrderItemRequest(BaseModel):
    product_id: UUID
    quantity: int = Field(..., gt=0)

class OrderCreateRequest(BaseModel):
    customer_id: UUID
    items: List[OrderItemRequest]

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreateRequest,
    service: OrderServiceInterface = Depends(get_order_service)
):
    # Convert Pydantic list of models to dictionary list for the service signature
    dict_items = [{"product_id": item.product_id, "quantity": item.quantity} for item in payload.items]
    return service.place_order(customer_id=payload.customer_id, items=dict_items)
