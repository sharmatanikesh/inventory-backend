from fastapi import APIRouter
from app.routers.product.create import router as create_router
from app.routers.product.get import router as get_router
from app.routers.product.list import router as list_router

product_router = APIRouter(prefix="/products", tags=["Products"])

# Mount individual method-specific routers
product_router.include_router(create_router)
product_router.include_router(get_router)
product_router.include_router(list_router)
