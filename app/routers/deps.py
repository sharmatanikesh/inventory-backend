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
    product_repo: ProductRepositoryInterface = Depends(get_product_repository)
) -> OrderServiceInterface:
    return OrderService(order_repo, product_repo)
