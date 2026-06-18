from fastapi import APIRouter, Depends, Query
from app.service.interfaces.product_service import ProductServiceInterface
from app.routers.deps import get_product_service

router = APIRouter()

@router.get("/")
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: ProductServiceInterface = Depends(get_product_service)
):
    # Route skeleton - delegates entirely to the interface-typed service
    return service.get_all_products(skip=skip, limit=limit)
