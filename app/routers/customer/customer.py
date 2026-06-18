from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, EmailStr, Field
from app.interfaces.customer import CustomerServiceInterface
from app.routers.deps import get_customer_service

router = APIRouter(prefix="/customers", tags=["Customers"])

class CustomerCreateRequest(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    email: EmailStr
    phone_number: Optional[str] = Field(None, max_length=50)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_customer(
    payload: CustomerCreateRequest,
    service: CustomerServiceInterface = Depends(get_customer_service)
):
    return service.register_customer(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        phone_number=payload.phone_number
    )


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


@router.get("/")
def list_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: CustomerServiceInterface = Depends(get_customer_service)
):
    return service.get_all_customers(skip=skip, limit=limit)
