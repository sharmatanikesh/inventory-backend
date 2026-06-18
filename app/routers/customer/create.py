from typing import Optional
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, EmailStr, Field
from app.service.interfaces.customer_service import CustomerServiceInterface
from app.routers.deps import get_customer_service

router = APIRouter()

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
