from fastapi import APIRouter
from app.routers.product.product import router as product_router
from app.routers.customer.customer import router as customer_router
from app.routers.order.order import router as order_router
from app.routers.dashboard.dashboard import router as dashboard_router
from app.routers.auth.router import auth_router

# Main API router uniting all route resource-modules
main_router = APIRouter()
main_router.include_router(auth_router)
main_router.include_router(product_router)
main_router.include_router(customer_router)
main_router.include_router(order_router)
main_router.include_router(dashboard_router)


