from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.service.interfaces.customer_service import CustomerServiceInterface
from app.routers.deps import get_customer_service

router = APIRouter()

@router.get("/{customer_id}")
def get_customer(
    customer_id: UUID,
    service: CustomerServiceInterface = Depends(get_customer_service)
):
    customer = service.get_customer(customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return customer
