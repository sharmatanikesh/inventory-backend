from fastapi import APIRouter
from app.routers.order.create import router as create_router
from app.routers.order.get import router as get_router
from app.routers.order.list import router as list_router

order_router = APIRouter(prefix="/orders", tags=["Orders"])

# Mount individual method-specific routers
order_router.include_router(create_router)
order_router.include_router(get_router)
order_router.include_router(list_router)
