from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, Query
from app.schemas.customer import CustomerCreateRequest, CustomerResponse
from app.utils.response import APIResponse
from app.controllers.customer import CustomerController
from app.routers.deps import get_customer_controller

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", status_code=201, response_model=APIResponse[CustomerResponse])
def create_customer(
    payload: CustomerCreateRequest,
    controller: CustomerController = Depends(get_customer_controller)
) -> APIResponse[CustomerResponse]:
    return controller.register_customer(payload)

@router.get("/{customer_id}", response_model=APIResponse[CustomerResponse])
def get_customer(
    customer_id: UUID,
    controller: CustomerController = Depends(get_customer_controller)
) -> APIResponse[CustomerResponse]:
    return controller.get_customer(customer_id)

@router.get("/", response_model=APIResponse[List[CustomerResponse]])
def list_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    controller: CustomerController = Depends(get_customer_controller)
) -> APIResponse[List[CustomerResponse]]:
    return controller.list_customers(skip=skip, limit=limit)

@router.delete("/{customer_id}", response_model=APIResponse[None])
def delete_customer(
    customer_id: UUID,
    controller: CustomerController = Depends(get_customer_controller)
) -> APIResponse[None]:
    return controller.delete_customer(customer_id)
