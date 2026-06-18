from fastapi import APIRouter, Depends, Query
from app.service.interfaces.customer_service import CustomerServiceInterface
from app.routers.deps import get_customer_service

router = APIRouter()

@router.get("/")
def list_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: CustomerServiceInterface = Depends(get_customer_service)
):
    return service.get_all_customers(skip=skip, limit=limit)
