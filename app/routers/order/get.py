from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.service.interfaces.order_service import OrderServiceInterface
from app.routers.deps import get_order_service

router = APIRouter()

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
