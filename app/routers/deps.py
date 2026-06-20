from uuid import UUID
from typing import Optional
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from app.database.database import get_db

# Repositories
from app.repository.product.repository import ProductRepositoryInterface, SQLAlchemyProductRepository
from app.repository.customer.repository import CustomerRepositoryInterface, SQLAlchemyCustomerRepository
from app.repository.order.repository import OrderRepositoryInterface, SQLAlchemyOrderRepository
from app.repository.user.repository import UserRepositoryInterface, SQLAlchemyUserRepository
from app.repository.refresh_token.repository import UserRefreshTokenRepositoryInterface, SQLAlchemyUserRefreshTokenRepository

# Services
from app.interfaces.product import ProductServiceInterface
from app.service.product.service import ProductService
from app.interfaces.customer import CustomerServiceInterface
from app.service.customer.service import CustomerService
from app.interfaces.order import OrderServiceInterface
from app.service.order.service import OrderService
from app.interfaces.auth import AuthServiceInterface
from app.service.auth.service import AuthService

# Controllers
from app.controllers.product import ProductController
from app.controllers.customer import CustomerController
from app.controllers.order import OrderController
from app.controllers.dashboard import DashboardController
from app.controllers.auth import AuthController

# Utils and Exceptions
from app.utils.auth import JWT_SECRET_KEY, JWT_ALGORITHM
from app.utils.exceptions import UnauthorizedException, ForbiddenException
from app.models.user import User


# ----------------- REPOSITORIES -----------------

def get_product_repository(db: Session = Depends(get_db)) -> ProductRepositoryInterface:
    return SQLAlchemyProductRepository(db)

def get_customer_repository(db: Session = Depends(get_db)) -> CustomerRepositoryInterface:
    return SQLAlchemyCustomerRepository(db)

def get_order_repository(db: Session = Depends(get_db)) -> OrderRepositoryInterface:
    return SQLAlchemyOrderRepository(db)

def get_user_repository(db: Session = Depends(get_db)) -> UserRepositoryInterface:
    return SQLAlchemyUserRepository(db)

def get_refresh_token_repository(db: Session = Depends(get_db)) -> UserRefreshTokenRepositoryInterface:
    return SQLAlchemyUserRefreshTokenRepository(db)


# ------------------- SERVICES -------------------

def get_product_service(
    repo: ProductRepositoryInterface = Depends(get_product_repository)
) -> ProductServiceInterface:
    return ProductService(repo)

def get_customer_service(
    repo: CustomerRepositoryInterface = Depends(get_customer_repository),
    user_repo: UserRepositoryInterface = Depends(get_user_repository)
) -> CustomerServiceInterface:
    return CustomerService(repo, user_repo)

def get_order_service(
    order_repo: OrderRepositoryInterface = Depends(get_order_repository),
    product_repo: ProductRepositoryInterface = Depends(get_product_repository),
    customer_repo: CustomerRepositoryInterface = Depends(get_customer_repository)
) -> OrderServiceInterface:
    return OrderService(order_repo, product_repo, customer_repo)

def get_auth_service(
    user_repo: UserRepositoryInterface = Depends(get_user_repository),
    token_repo: UserRefreshTokenRepositoryInterface = Depends(get_refresh_token_repository)
) -> AuthServiceInterface:
    return AuthService(user_repo, token_repo)


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

def get_dashboard_controller(
    product_repo: ProductRepositoryInterface = Depends(get_product_repository),
    customer_repo: CustomerRepositoryInterface = Depends(get_customer_repository),
    order_repo: OrderRepositoryInterface = Depends(get_order_repository)
) -> DashboardController:
    return DashboardController(product_repo, customer_repo, order_repo)

def get_auth_controller(
    service: AuthServiceInterface = Depends(get_auth_service)
) -> AuthController:
    return AuthController(service)


# ---------------- SECURITY DEPENDENCIES ----------------

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    user_repo: UserRepositoryInterface = Depends(get_user_repository)
) -> User:
    if not token:
        raise UnauthorizedException("Access token not provided. Please login.")
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id_str: str = payload.get("sub")
        if not user_id_str:
            raise UnauthorizedException("Invalid access token claims.")
        user_id = UUID(user_id_str)
    except jwt.PyJWTError:
        raise UnauthorizedException("Expired or invalid access token. Please refresh.")
        
    user = user_repo.get_by_id(user_id)
    if not user or not user.is_active:
        raise UnauthorizedException("User not found or account is deactivated.")
    return user

def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != "ADMIN":
        raise ForbiddenException("Admin privilege required for this resource.")
    return current_user

def get_current_customer(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != "CUSTOMER":
        raise ForbiddenException("Customer privilege required for this resource.")
    return current_user
