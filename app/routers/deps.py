from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.database import get_db

# Repositories
from app.repository.product_repository import ProductRepositoryInterface, SQLAlchemyProductRepository
from app.repository.customer_repository import CustomerRepositoryInterface, SQLAlchemyCustomerRepository
from app.repository.order_repository import OrderRepositoryInterface, SQLAlchemyOrderRepository

# Services
from app.service.interfaces.product_service import ProductServiceInterface
from app.service.impl.product_service import ProductService
from app.service.interfaces.customer_service import CustomerServiceInterface
from app.service.impl.customer_service import CustomerService
from app.service.interfaces.order_service import OrderServiceInterface
from app.service.impl.order_service import OrderService

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
