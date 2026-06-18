from fastapi import APIRouter, Depends, Query
from app.service.interfaces.order_service import OrderServiceInterface
from app.routers.deps import get_order_service

router = APIRouter()

@router.get("/")
def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: OrderServiceInterface = Depends(get_order_service)
):
    return service.get_all_orders(skip=skip, limit=limit)
