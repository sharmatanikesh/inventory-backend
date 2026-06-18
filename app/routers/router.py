from fastapi import APIRouter
from app.routers.product.router import product_router
from app.routers.customer.router import customer_router
from app.routers.order.router import order_router

# Main API router uniting all route resource-modules
main_router = APIRouter()
main_router.include_router(product_router)
main_router.include_router(customer_router)
main_router.include_router(order_router)
