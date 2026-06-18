from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.product import Product

class ProductRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        """Retrieve a product by its ID."""
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Retrieve all active products with pagination."""
        pass

    @abstractmethod
    def create(self, name: str, sku: str, price: float, quantity: int) -> Product:
        """Create and persist a new product."""
        pass

    @abstractmethod
    def update_quantity(self, product_id: UUID, quantity: int) -> Optional[Product]:
        """Update product quantity/stock level."""
        pass


class SQLAlchemyProductRepository(ProductRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        # Implementation skeleton - actual db query code excluded
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        # Implementation skeleton - actual db query code excluded
        pass

    def create(self, name: str, sku: str, price: float, quantity: int) -> Product:
        # Implementation skeleton - actual db query code excluded
        pass

    def update_quantity(self, product_id: UUID, quantity: int) -> Optional[Product]:
        # Implementation skeleton - actual db query code excluded
        pass
