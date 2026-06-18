from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from app.interfaces.order import OrderServiceInterface
from app.routers.deps import get_order_service

router = APIRouter(prefix="/orders", tags=["Orders"])

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
    dict_items = [{"product_id": item.product_id, "quantity": item.quantity} for item in payload.items]
    return service.place_order(customer_id=payload.customer_id, items=dict_items)


@router.get("/{order_id}")
def get_order(
    order_id: UUID,
    service: OrderServiceInterface = Depends(get_order_service)
):
    order = service.get_order(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order


@router.get("/")
def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: OrderServiceInterface = Depends(get_order_service)
):
    return service.get_all_orders(skip=skip, limit=limit)
