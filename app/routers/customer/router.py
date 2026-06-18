from fastapi import APIRouter
from app.routers.customer.create import router as create_router
from app.routers.customer.get import router as get_router
from app.routers.customer.list import router as list_router

customer_router = APIRouter(prefix="/customers", tags=["Customers"])

# Mount individual method-specific routers
customer_router.include_router(create_router)
customer_router.include_router(get_router)
customer_router.include_router(list_router)
