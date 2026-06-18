from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from app.interfaces.product import ProductServiceInterface
from app.routers.deps import get_product_service

router = APIRouter(prefix="/products", tags=["Products"])

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
    return service.create_product(
        name=payload.name,
        sku=payload.sku,
        price=payload.price,
        quantity=payload.quantity
    )


@router.get("/{product_id}")
def get_product(
    product_id: UUID,
    service: ProductServiceInterface = Depends(get_product_service)
):
    product = service.get_product(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.get("/")
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: ProductServiceInterface = Depends(get_product_service)
):
    return service.get_all_products(skip=skip, limit=limit)
