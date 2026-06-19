from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.database import get_db

# Repositories
from app.repository.product.repository import ProductRepositoryInterface, SQLAlchemyProductRepository
from app.repository.customer.repository import CustomerRepositoryInterface, SQLAlchemyCustomerRepository
from app.repository.order.repository import OrderRepositoryInterface, SQLAlchemyOrderRepository

# Services
from app.interfaces.product import ProductServiceInterface
from app.service.product.service import ProductService
from app.interfaces.customer import CustomerServiceInterface
from app.service.customer.service import CustomerService
from app.interfaces.order import OrderServiceInterface
from app.service.order.service import OrderService

# Controllers
from app.controllers.product import ProductController
from app.controllers.customer import CustomerController
from app.controllers.order import OrderController
from app.controllers.dashboard import DashboardController


# ----------------- REPOSITORIES -----------------

def get_product_repository(db: Session = Depends(get_db)) -> ProductRepositoryInterface:
    return SQLAlchemyProductRepository(db)

def get_customer_repository(db: Session = Depends(get_db)) -> CustomerRepositoryInterface:
    return SQLAlchemyCustomerRepository(db)

def get_order_repository(db: Session = Depends(get_db)) -> OrderRepositoryInterface:
    return SQLAlchemyOrderRepository(db)

# ------------------- SERVICES -------------------

def get_product_service(
    repo: ProductRepositoryInterface = Depends(get_product_repository)
) -> ProductServiceInterface:
    return ProductService(repo)

def get_customer_service(
    repo: CustomerRepositoryInterface = Depends(get_customer_repository)
) -> CustomerServiceInterface:
    return CustomerService(repo)

def get_order_service(
    order_repo: OrderRepositoryInterface = Depends(get_order_repository),
    product_repo: ProductRepositoryInterface = Depends(get_product_repository),
    customer_repo: CustomerRepositoryInterface = Depends(get_customer_repository)
) -> OrderServiceInterface:
    return OrderService(order_repo, product_repo, customer_repo)

# ----------------- CONTROLLERS -----------------

def get_product_controller(
    service: ProductServiceInterface = Depends(get_product_service)
) -> ProductController:
    return ProductController(service)

def get_customer_controller(
    service: CustomerServiceInterface = Depends(get_customer_service)
) -> CustomerController:
    return CustomerController(service)

def get_order_controller(
    service: OrderServiceInterface = Depends(get_order_service)
) -> OrderController:
    return OrderController(service)

def get_dashboard_controller() -> DashboardController:
    return DashboardController()
