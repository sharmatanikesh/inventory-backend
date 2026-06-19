from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, Query
from app.schemas.product import ProductCreateRequest, ProductResponse
from app.utils.response import APIResponse
from app.controllers.product import ProductController
from app.routers.deps import get_product_controller

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", status_code=201, response_model=APIResponse[ProductResponse])
def create_product(
    payload: ProductCreateRequest,
    controller: ProductController = Depends(get_product_controller)
) -> APIResponse[ProductResponse]:
    return controller.create_product(payload)

@router.get("/{product_id}", response_model=APIResponse[ProductResponse])
def get_product(
    product_id: UUID,
    controller: ProductController = Depends(get_product_controller)
) -> APIResponse[ProductResponse]:
    return controller.get_product(product_id)

@router.get("/", response_model=APIResponse[List[ProductResponse]])
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    controller: ProductController = Depends(get_product_controller)
) -> APIResponse[List[ProductResponse]]:
    return controller.list_products(skip=skip, limit=limit)

@router.put("/{product_id}", response_model=APIResponse[ProductResponse])
def update_product(
    product_id: UUID,
    payload: ProductCreateRequest,
    controller: ProductController = Depends(get_product_controller)
) -> APIResponse[ProductResponse]:
    return controller.update_product(product_id, payload)

@router.delete("/{product_id}", response_model=APIResponse[None])
def delete_product(
    product_id: UUID,
    controller: ProductController = Depends(get_product_controller)
) -> APIResponse[None]:
    return controller.delete_product(product_id)
