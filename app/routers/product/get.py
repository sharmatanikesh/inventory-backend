from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.service.interfaces.product_service import ProductServiceInterface
from app.routers.deps import get_product_service

router = APIRouter()

@router.get("/{product_id}")
def get_product(
    product_id: UUID,
    service: ProductServiceInterface = Depends(get_product_service)
):
    # Route skeleton - delegates entirely to the interface-typed service
    product = service.get_product(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product
