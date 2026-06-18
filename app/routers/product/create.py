from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from app.service.interfaces.product_service import ProductServiceInterface
from app.routers.deps import get_product_service

router = APIRouter()

class ProductCreateRequest(BaseModel):
    name: str = Field(..., max_length=255)
    sku: str = Field(..., max_length=100)
    price: float = Field(..., gt=0.0)
    quantity: int = Field(..., ge=0)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreateRequest,
    service: ProductServiceInterface = Depends(get_product_service)
):
    # Route skeleton - delegates entirely to the interface-typed service
    return service.create_product(
        name=payload.name,
        sku=payload.sku,
        price=payload.price,
        quantity=payload.quantity
    )
