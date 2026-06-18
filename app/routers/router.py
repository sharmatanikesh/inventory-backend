from fastapi import APIRouter
from app.routers.product.product import router as product_router
from app.routers.customer.customer import router as customer_router
from app.routers.order.order import router as order_router

# Main API router uniting all route resource-modules
main_router = APIRouter()
main_router.include_router(product_router)
main_router.include_router(customer_router)
main_router.include_router(order_router)

