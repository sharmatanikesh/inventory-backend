from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, Query
from app.schemas.order import OrderCreateRequest, OrderResponse
from app.utils.response import APIResponse
from app.controllers.order import OrderController
from app.routers.deps import get_order_controller

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", status_code=201, response_model=APIResponse[OrderResponse])
def create_order(
    payload: OrderCreateRequest,
    controller: OrderController = Depends(get_order_controller)
) -> APIResponse[OrderResponse]:
    return controller.place_order(payload)

@router.get("/{order_id}", response_model=APIResponse[OrderResponse])
def get_order(
    order_id: UUID,
    controller: OrderController = Depends(get_order_controller)
) -> APIResponse[OrderResponse]:
    return controller.get_order(order_id)

@router.get("/", response_model=APIResponse[List[OrderResponse]])
def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    controller: OrderController = Depends(get_order_controller)
) -> APIResponse[List[OrderResponse]]:
    return controller.list_orders(skip=skip, limit=limit)

@router.delete("/{order_id}", response_model=APIResponse[OrderResponse])
def cancel_order(
    order_id: UUID,
    controller: OrderController = Depends(get_order_controller)
) -> APIResponse[OrderResponse]:
    return controller.cancel_order(order_id)
